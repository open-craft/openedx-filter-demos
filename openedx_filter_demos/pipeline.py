"""
Module that contains the openedx_filters pipeline steps.
"""
import json
import logging

from openedx_filters import PipelineStep

logger = logging.getLogger(__name__)


class AddDebugInfoBlock(PipelineStep):
    """
    Adds extra HTML to the fragment.

    Example Usage:

    .. code-block::

        "OPENEDX_FILTERS_CONFIG": {
            "org.openedx.learning.vertical_block.render.completed.v1": {
                "fail_sliently": false,
                "pipeline": [
                    "openedx_filter_demos.pipeline.AddDebugInfo"
                ]
            }
        }
    """

    def run_filter(self, block, fragment, context, view):
        """Pipeline Step implementing the Filter"""

        debug_div = f"""<div class="debug-block" style="border: 2px solid red; padding: 1rem; margin: 1rem;">
<h5>Debug Info</h5>
<pre>
block = {str(block)}
fragment = {str(fragment)}
context = {json.dumps(context, indent=2)}
view = {view}
</pre>
</div>
"""
        fragment.content = f"""<div class="openedx-filter-demos">{fragment.content}{debug_div}</div>"""

        logger.info("=========== AddDebugInfoBlock Pipeline Step Start ==========")
        logger.info("Fragment: %s", str(fragment))
        logger.info("Context: %s", context)
        logger.info("View: %s", view)
        logger.info("=========== AddDebugInfoBlock Pipeline Step End ==========")

        return {"block": block, "fragment": fragment, "context": context, "view": view}


class AddAJAXButtonBlock(PipelineStep):
    """
    Injects an button and JS for making a AJAX POST request to the "dummy_json" JSON Handler of the XBlock.

    So, add a JSON like the one below to your XBlock before adding this step to your filter pipeline.

    .. code-block::

        @XBlock.json_handler
        def dummy_json(self, data, suffix=""):
            print("[DUMMY JSON Handler]")
            print(f"Data passed to the endpoint: {data}")
            return {"status": "success"}

    Example Configuration:

    .. code-block::

        "OPENEDX_FILTERS_CONFIG": {
            "org.openedx.learning.vertical_block.render.completed.v1": {
                "fail_silently": false,
                "pipeline": [
                    "openedx_filter_demos.pipeline.AddAJAXButton"
                ]
            }
        }
    """
    def run_filter(self, block, fragment, context, view):
        """
        Pipeline step implementing the filter.
        """
        url = block.runtime.handler_url(block, "dummy_json")
        script = """
<script>
function callDummyJsonHandler(url) {
    var csrf_token = document.cookie.split(";").find(c => c.startsWith("csrftoken="))?.split("=")[1];
    fetch(url, {
        method: "POST",
        body: JSON.stringify(["some", "data"]), 
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token,
        }
    })
    .then(res => res.json())
    .then(data => document.querySelector("#response").innerHTML = JSON.stringify(data));
}
</script>
"""
        snippet = f"""<div class="debug-block" style="border: 2px solid red; padding 1rem; margin: 1rem;">
<h5>Ajax Demo</h5>
<p><strong>NOTE!</strong> This requires a "dummy_json" JSON Handler to be defined in the VerticalBlock to test.</p>
<button onclick="callDummyJsonHandler('{str(url)}')">Send Data</button>

<h5 style="maring-top: 1rem;">Response</h5>
<pre id="response"></pre>
{script}
</div>
"""
        fragment.content = f"""<div class="openedx-filter-demos">{fragment.content}{snippet}</div>"""

        return dict(block=block, fragment=fragment, context=context, view=view)
