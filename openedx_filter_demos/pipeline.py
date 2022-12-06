"""
Module that contains the openedx_filters pipeline steps.
"""
import json
import logging

from openedx_filters import PipelineStep

logger = logging.getLogger(__name__)


class AddExtraBlock(PipelineStep):
    """
    Adds an block at the end of a VerticalBlock.

    Example Usage:

    .. code-block::

        "OPENEDX_FILTERS_CONFIG": {
            "org.openedx.learning.vertical_block.render.completed.v1": {
                "fail_sliently": false,
                "pipeline": [
                    "openedx_filter_demos.pipeline.AddExtraBlock"
                ]
            }
        }
    """

    def run_filter(self, fragment, context, view):
        """Pipeline Step implementing the Filter"""

        debug_div = f"""<div class="debug-block" style="border: 2px solid red; padding: 1rem; margin: 1rem;">
<pre>
fragment = {fragment}
context = {json.dumps(context, indent=2)}
view = {view}
</pre>
</div>
"""
        fragment.content = f"""<div class="openedx-filter-demos">{fragment.content}{debug_div}</div>"""

        logger.info("=========== AddExtraBlock Pipeline Step Start ==========")
        logger.info("Fragment: %s", str(fragment))
        logger.info("Context: %s", context)
        logger.info("View: %s", view)
        logger.info("=========== AddExtraBlock Pipeline Step Stop ==========")

        return {"fragment": fragment, "context": context, "view": view}
