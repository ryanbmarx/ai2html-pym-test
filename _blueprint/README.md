Tribune P2P Tarbell Blueprint
=============================

A [Tarbell Blueprint](http://tarbell.readthedocs.org/en/latest/build.html#understanding-tarbell-blueprints) for publishing spreadsheet-driven news applications, data visualizations or stories to P2P htmlstory content types.

Assumptions
-----------

* Python 2.7
* Tarbell 1.0.\*
* Node.js
* grunt-cli (See http://gruntjs.com/getting-started#installing-the-cli)

Custom configuration
--------------------

You should define the following keys in either the `values` worksheet of the Tarbell spreadsheet or the `DEFAULT_CONTEXT` setting in your `tarbell_config.py`:

* p2p\_slug
* headline 
* seotitle
* seodescription
* keywords
* byline

Note that these will clobber any values set in P2P each time the project is republished.  

Publishing
----------

When publishing to production (`tarbell publish production`), the P2P content item specified in the `p2p_slug` value in the spreadsheet or `DEFAULT_CONTEXT` setting will be created or updated with the rendered page.

If you want to disable the creation or updating of the P2P content item, just remove the `p2p_slug` key/value from the spreadsheet and `DEFAULT_CONTEXT` setting.  This is a rare case, but you might want to use it if you're only publishing blurbs that will be embedded in another story, or want to publish using a separate script instead of the blueprint's default method.  Remember that assets (CSS, JavaScript, etc.) will still get published to S3.

Publishing to P2P
-----------------

By default, this blueprint will render the content in `_hmtlstory.html` and publish it to a HTML story in P2P.  JavaScript, CSS, images and any custom data will be published to S3, as with any Tarbell project.

To override the P2P publishing behavior, define a hook function and set the `P2P_PUBLISH_HOOK` variable in your `tarbell_config.py` to this function.


Building front-end assets
-------------------------

This blueprint creates configuration to use [Grunt](http://gruntjs.com/) to build front-end assets.

When you create a new Tarbell project using this blueprint with `tarbell newproject`, you will be prompted about whether you want to use [Sass](http://sass-lang.com/) to generate CSS and whether you want to use  [Browserify](http://browserify.org/) to bundle JavaScript from multiple files.  Based on your input, the blueprint will generate a `package.json` and `Gruntfile.js` with the appropriate configuration.

After creating the project, run:

    npm install

to install the build dependencies for our front-end assets.

When you run:

    grunt

Grunt will compile `sass/styles.scss` into `css/styles.css` and bundle/minify `js/src/app.js` into `js/app.min.js`.

If you want to recompile as you develop, run:

    grunt && grunt watch

This blueprint simply sets up the the build tools to generate `styles.css` and `js/app.min.js`, you'll have to explicitly update your templates to point to these generated files.  The reason for this is to make you think about whether you're actually going to use an external CSS or JavaScript file and avoid a request for an empty file if you don't end up putting anything in your custom stylesheet or JavaScript file.

To add `app.min.js` to your template file:

    {% block scripts %}
    <script src="js/app.min.js"></script>
    {% endblock %}

Tests
-----

To run unit tests for this blueprint, run:

    python -m unittest tests.test_blueprint_utils
