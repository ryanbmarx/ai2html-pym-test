# Testing NPR rig for AI2html

A [Tarbell](http://tarbell.io) project that publishes to a P2P HTML Story.


<< Cue the [music](https://www.youtube.com/watch?v=9N__4oE0Afs) >>

Dear David,

I continue my struggles with the resizing iframes. You'll find that I've made changes to NYT's resizer script, removing most of their specific stuff and the immediately-executed inline function construction. I'm left with `resizer()`, which does what it should, and `throttle()`, which is code jacked from Underscore.

I've also removed the event listeners into the body of the graphic, which I feel is a better place for them.

Your help is super appreciated.

Sincerest regard, 
Cpl. Ryan Marx,
Third Illinois Infantry

P.S. Don't forget to `npm install` and `npm run build`. The good lord above know that solves about 90% of the problems around here that start with "Hey, Ryan, I broke it."






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

    
    <script src="js/app.min.js"></script>
    