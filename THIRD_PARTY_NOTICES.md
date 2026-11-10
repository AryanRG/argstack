# Source and license map

The root MIT license applies to original argstack material only. Each bundled upstream skill retains its own license and notices.

- **tstack (MIT, Theo Browne)**: file-pr, modernize, council. Adapted from [t3dotgg/tstack at 1085050f](https://github.com/t3dotgg/tstack/tree/1085050f3baed1ac724caa4a8166145fb2ac88af). Changes cover explicit provider and billing selection, bounded reviews, and publication scope.
- **pstack (MIT, Lauren Tan)**: bro, how, ketchup, ketchup-video, statechart, unslop. From [cursor/plugins at de8ee15d](https://github.com/cursor/plugins/tree/de8ee15dd1194627d21eb5fcd41cb1873208dabb/pstack). Some entries are adapted for multiple harnesses, local rendering and optional delegation. The statechart runtime is included; upstream test fixtures and external toolchains are not.
- **Anthropic Skills (Apache 2.0)**: docx, pdf, pptx, xlsx, frontend-design, mcp-builder, webapp-testing. Unmodified skill folders from the [public upstream revision 2c5958ec](https://github.com/anthropics/skills/tree/2c5958ecac7cee2b583967a2c4981d0f4a75c579/skills), with their LICENSE.txt files and the publisher’s [third-party notices](anthropic-notices.md).
- **doc-coauthoring**: optional upstream install from that same revision. Its folder has no separate license file, so this repository links to the publisher and does not redistribute the text.
- **argstack**: overnight and app-demo-video are locally authored. Overnight draws on the autonomous-run and never-block-on-the-human ideas in pstack; the implementation is original. The demo renderer calls separately installed tools. No voice weights, upstream API credentials, or app recordings are distributed.
