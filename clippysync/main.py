
import iroh
import argparse
import asyncio
import clipman

async def sync_clipboard(doc, node, author):
    # Storage for latest known clipboard data
    _CLIPBOARD = None

    # Initialize clipman
    clipman.init()

    # Watch for updates locally and from Iroh
    while True:
        # Probably don't need clipboard data that often
        await asyncio.sleep(1)

        # Check clipman locally
        try:
            clipboard_data = clipman.get()
        except clipman.exceptions.ClipmanBaseException as e:
            print("Clipman error:", e)
            continue

        # Check Iroh for clipboard data
        try:
            query = iroh.Query.single_latest_per_key_exact(b"clip")
            entry = await doc.get_one(query)
            hash = entry.content_hash()
            content = await node.blobs().read_to_bytes(hash)
            iroh_data = content.decode("utf8")
        except iroh.iroh_ffi.IrohError as e:
            print("Iroh error:", e)
            continue

        # If _CLIPBAORD is the same as iroh_date, and clipboard_data is not the same as _CLIPBOARD, then update _CLIPBOARD and iroh_data
        if _CLIPBOARD == iroh_data and clipboard_data != _CLIPBOARD:
            _CLIPBOARD = clipboard_data
            await doc.set_bytes(author, b'clip', clipboard_data.encode())
            print(f"Sent clipboard data to Iroh ({clipboard_data})")
        # If _CLIPBOARD is not the same as iroh_data, then update _CLIPBOARD to iroh_data
        elif _CLIPBOARD != iroh_data:
            _CLIPBOARD = iroh_data
            clipman.set(iroh_data)
            print(f"Received clipboard data from Iroh ({iroh_data})")


async def main():
    # setup event loop, to ensure async callbacks work
    iroh.iroh_ffi.uniffi_set_event_loop(asyncio.get_running_loop())

    # parse arguments
    parser = argparse.ArgumentParser(description='A tool for syncing clipboards across multiple machines')
    parser.add_argument('--ticket', type=str, help='ticket to join a clipboard document')
    args = parser.parse_args()

    # create iroh node
    options = iroh.NodeOptions()
    options.enable_docs = True
    node = await iroh.Iroh.memory_with_options(options)
    node_id = await node.net().node_id()
    print("Started Iroh node: {}".format(node_id))

    # If no ticket is provided, create a new document and share it
    if not args.ticket:
        # create doc
        doc = await node.docs().create()
        author = await node.authors().create()
        doc_id = doc.id()

        # create ticket to share doc
        ticket = await doc.share(iroh.ShareMode.WRITE, iroh.AddrInfoOptions.RELAY_AND_ADDRESSES)

        # add data to doc
        await doc.set_bytes(author, b"clip", b"ClippySync is awesome!")
        print("Created doc: {}".format(doc_id))
        print("Keep this running and on other computers run:\n\npython main.py --ticket {}".format(ticket))
    
    # If a ticket is provided, join the document
    else:
        # join doc
        doc_ticket = iroh.DocTicket(args.ticket)
        doc = await node.docs().join(doc_ticket)
        doc_id = doc.id()
        print("Joined doc: {}".format(doc_id))
        author = await node.authors().create()

        # sync & print
        print("Waiting 5 seconds to let stuff sync...")
        await asyncio.sleep(5)

    # Start syncing the clipboard
    await sync_clipboard(doc, node, author)

if __name__ == "__main__":
    asyncio.run(main())
