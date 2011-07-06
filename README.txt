Cookie Audit
============

Ed Crewe, 4 July 2011

UK and European Cookie laws
---------------------------

The current UK Law requires full compliance by May 2012

http://www.ico.gov.uk/news/current_topics/website_changes_pecr.aspx

Auditing tools
--------------

The main audit tool that is currently available is browser based only

http://www.primelife.eu/results/opensource/76-dashboard

a plugin for Firefox. Although very useful it is not so suited to a
full automatic audit of a website, since it is dependent on the user manually 
clicking around the site. 

It could potentially be automated by, for example, installing the plugin then
driving Firefox with spidering system* and the privacy dashboard plugin across a whole site, 
but this seems a rather top heavy inelegant way of doing it, when spiders themselves
can retrieve the cookies.

This software is a set of configuration scripts for one such spider, Scrapy.

http://scrapy.org/ 

Installation details on the site, or alternatively install fabric and virtualenv
then run the fabfile in this directory.

* Scrapy has the option to use Firefox as its client for crawls, 
  alternatively Selenium could also be used to drive it.    

Auditing your domain
--------------------

The aim of this package is to provide a crawler that will 
provide a full audit of cookie usage across a domain.

As a first step in ensuring compliance with UK law by the deadline.


 
