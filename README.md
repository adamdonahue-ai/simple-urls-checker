A simple script that checks the status code of each URL in a list of URLs
and prints to stdout whether the status code returned is one of the
list of status codes provided, or otherwise reports an error.

Note that there is no throttling, so if we hammer thousands of endpoints
with the default settings we might get issues.  A delay or some other
logic would probably help here.  I didn't go crazy with optimizations.

I grabbed a bunch of URLs into a file with a quick one-liner:

```
(simple-urls-checker) adamdonahue@Adams-MacBook-Air simple-urls-checker % curl https://downloads.majestic.com/majestic_million.csv | tail -n +2 | cut -d, -f3  | awk '{ print "https://" $1 }' > /tmp/urls
```

You can then run via Docker easily enough using -v to mount the urls.  Some sample input follows (truncated).

```
(simple-urls-checker) adamdonahue@Adams-MacBook-Air simple-urls-checker % docker build -t urls-checker:latest .
(simple-urls-checker) adamdonahue@Adams-MacBook-Air simple-urls-checker % docker run -v /tmp:/foo urls-checker --urls-file /foo/urls
OK     https://github.com  [200]  retries=0
OK     https://en.wikipedia.org  [200]  retries=0
OK     https://wordpress.org  [200]  retries=0
OK     https://vimeo.com  [200]  retries=0
OK     https://wikipedia.org  [200]  retries=0
OK     https://apple.com  [200]  retries=0
ERROR  https://googletagmanager.com  [HTTP 404]  retries=3
OK     https://apps.apple.com  [200]  retries=0
OK     https://google.com  [200]  retries=0
OK     https://facebook.com  [200]  retries=0
OK     https://pinterest.com  [200]  retries=0
OK     https://play.google.com  [200]  retries=0
OK     https://instagram.com  [200]  retries=0
OK     https://linkedin.com  [200]  retries=0
OK     https://youtube.com  [200]  retries=0
OK     https://youtu.be  [200]  retries=0
OK     https://nginx.org  [200]  retries=0
ERROR  https://twitter.com  [400, message='Got more than 8190 bytes (9822) when reading Header value is too long.', url='https://twitter.com']  retries=3
OK     https://wordpress.com  [200]  retries=0
OK     https://whatsapp.com  [200]  retries=0
OK     https://policies.google.com  [200]  retries=0
OK     https://docs.google.com  [200]  retries=0
ERROR  https://amazon.com  [HTTP 202]  retries=3
OK     https://bit.ly  [200]  retries=0
ERROR  https://x.com  [400, message='Got more than 8190 bytes (9822) when reading Header value is too long.', url='https://x.com']  retries=3
OK     https://api.whatsapp.com  [200]  retries=0
OK     https://wa.me  [200]  retries=0
ERROR  https://goo.gl  [HTTP 400]  retries=3
OK     https://apache.org  [200]  retries=0
OK     https://plus.google.com  [200]  retries=0
OK     https://f5.com  [200]  retries=0
OK     https://player.vimeo.com  [200]  retries=0
OK     https://gravatar.com  [200]  retries=0
OK     https://github.io  [200]  retries=0
ERROR  https://miit.gov.cn  [Cannot connect to host miit.gov.cn:443 ssl:default [Name or service not known]]  retries=3
OK     https://itunes.apple.com  [200]  retries=0
OK     https://maps.google.com  [200]  retries=0
OK     https://nginx.com  [200]  retries=0
OK     https://drive.google.com  [200]  retries=0
OK     https://mailinabox.email  [200]  retries=0
OK     https://tumblr.com  [200]  retries=0
OK     https://nih.gov  [200]  retries=0
OK     https://mozilla.org  [200]  retries=0
OK     https://support.google.com  [200]  retries=0
OK     https://blogspot.com  [200]  retries=0
ERROR  https://microsoft.com  [HTTP 403]  retries=3
OK     https://europa.eu  [200]  retries=0
OK     https://flickr.com  [200]  retries=0
OK     https://archive.org  [200]  retries=0
ERROR  https://reddit.com  [HTTP 403]  retries=3
ERROR  https://maps.app.goo.gl  [HTTP 400]  retries=3
OK     https://t.me  [200]  retries=0
OK     https://open.spotify.com  [200]  retries=0
OK     https://spotify.com  [200]  retries=0
OK     https://yahoo.com  [200]  retries=0
OK     https://office.com  [200]  retries=0
OK     https://sites.google.com  [200]  retries=0
OK     https://creativecommons.org  [200]  retries=0
ERROR  https://forms.gle  [HTTP 400]  retries=3
OK     https://w3.org  [200]  retries=0
OK     https://www.ncbi.nlm.nih.gov  [200]  retries=0
OK     https://tiktok.com  [200]  retries=0
OK     https://nytimes.com  [200]  retries=0
OK     https://soundcloud.com  [200]  retries=0
OK     https://forbes.com  [200]  retries=0
ERROR  https://godaddy.com  [HTTP 403]  retries=3
ERROR  https://wixsite.com  [Cannot connect to host wixsite.com:443 ssl:default [Name or service not known]]  retries=3
ERROR  https://medium.com  [HTTP 403]  retries=3
OK     https://sourceforge.net  [200]  retries=0
OK     https://zoom.us  [200]  retries=0
OK     https://doi.org  [200]  retries=0
OK     https://web.archive.org  [200]  retries=0
OK     https://shopify.com  [200]  retries=0
OK     https://cpanel.net  [200]  retries=0
OK     https://ec.europa.eu  [200]  retries=0
OK     https://t.co  [200]  retries=0
ERROR  https://amazonaws.com  [Cannot connect to host amazonaws.com:443 ssl:default [Connect call failed ('72.21.206.80', 443)]]  retries=3
OK     https://tinyurl.com  [200]  retries=0
ERROR  https://youtube-nocookie.com  [Cannot connect to host youtube-nocookie.com:443 ssl:True [SSLCertVerificationError: (1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostname mismatch, certificate is not valid for 'youtube-nocookie.com'. (_ssl.c:1032)")]]  retries=3
OK     https://cnn.com  [200]  retries=0
OK     https://accounts.google.com  [200]  retries=0
OK     https://launchpad.net  [200]  retries=0
OK     https://dropbox.com  [200]  retries=0
OK     https://dropcatch.com  [200]  retries=0
OK     https://theguardian.com  [200]  retries=0
OK     https://bbc.com  [200]  retries=0
OK     https://opera.com  [200]  retries=0
OK     https://php.net  [200]  retries=0
OK     https://qq.com  [200]  retries=0
ERROR  https://who.int  [400, message='Got more than 8190 bytes (8742) when reading Header value is too long.', url='https://www.who.int/']  retries=3
OK     https://bbc.co.uk  [200]  retries=0
OK     https://cloudflare.com  [200]  retries=0
OK     https://harvard.edu  [200]  retries=0
OK     https://bing.com  [200]  retries=0
OK     https://googleblog.com  [200]  retries=0
OK     https://mit.edu  [200]  retries=0
OK     https://issuu.com  [200]  retries=0
ERROR  https://researchgate.net  [HTTP 403]  retries=3
ERROR  https://sciencedirect.com  [HTTP 403]  retries=3
OK     https://cdc.gov  [200]  retries=0
ERROR  https://oracle.com  [HTTP 403]  retries=3
OK     https://paypal.com  [200]  retries=0
OK     https://wikimedia.org  [200]  retries=0
ERROR  https://gnu.org  [HTTP 403]  retries=3
OK     https://ibm.com  [200]  retries=0
OK     https://linktr.ee  [200]  retries=0
OK     https://un.org  [200]  retries=0
OK     https://debian.org  [200]  retries=0
OK     https://wiley.com  [200]  retries=0
ERROR  https://imdb.com  [HTTP 202]  retries=3
OK     https://pubmed.ncbi.nlm.nih.gov  [200]  retries=0
ERROR  https://reuters.com  [HTTP 401]  retries=3
OK     https://weebly.com  [200]  retries=0
OK     https://plesk.com  [200]  retries=0
OK     https://vk.com  [200]  retries=0
OK     https://workspaceupdates.googleblog.com  [200]  retries=0
OK     https://discord.com  [200]  retries=0
ERROR  https://beian.gov.cn  [Cannot connect to host beian.gov.cn:443 ssl:default [Name or service not known]]  retries=3
OK     https://example.com  [200]  retries=0
OK     https://discord.gg  [200]  retries=0
OK     https://www.gov.uk  [200]  retries=0
OK     https://msn.com  [200]  retries=0
OK     https://stanford.edu  [200]  retries=0
OK     https://nasa.gov  [200]  retries=0
OK     https://springer.com  [200]  retries=0
OK     https://cookiedatabase.org  [200]  retries=0
ERROR  https://cloudfront.net  [Cannot connect to host cloudfront.net:443 ssl:default [Name or service not known]]  retries=3
OK     https://outlook.com  [200]  retries=0
OK     https://nature.com  [200]  retries=0
OK     https://businessinsider.com  [200]  retries=0
ERROR  https://wsj.com  [HTTP 401]  retries=3
OK     https://calendly.com  [200]  retries=0
ERROR  https://bloomberg.com  [HTTP 403]  retries=3
OK     https://telegram.me  [200]  retries=0
OK     https://baidu.com  [200]  retries=0
OK     https://ietf.org  [200]  retries=0
ERROR  https://amzn.to  [HTTP 202]  retries=3
ERROR  https://expireddomains.com  [HTTP 403]  retries=3
OK     https://g.page  [200]  retries=0
OK     https://mp.weixin.qq.com  [200]  retries=0
OK     https://addtoany.com  [200]  retries=0
OK     https://cnbc.com  [200]  retries=0
OK     https://twitch.tv  [200]  retries=0
ERROR  https://etsy.com  [HTTP 403]  retries=3
ERROR  https://unsplash.com  [HTTP 401]  retries=3
OK     https://wired.com  [200]  retries=0
OK     https://gitlab.com  [200]  retries=0
OK     https://time.com  [200]  retries=0
OK     https://eventbrite.com  [200]  retries=0
ERROR  https://mysql.com  [HTTP 403]  retries=3
ERROR  https://canva.com  [HTTP 403]  retries=3
ERROR  https://googleusercontent.com  [HTTP 404]  retries=3
ERROR  https://myshopify.com  [HTTP 404]  retries=3
OK     https://behance.net  [200]  retries=0
ERROR  https://wpa.qq.com  [HTTP 403]  retries=3
OK     https://weibo.com  [200]  retries=0
OK     https://npr.org  [200]  retries=0
OK     https://line.me  [200]  retries=0
OK     https://go.com  [200]  retries=0
OK     https://stripe.com  [200]  retries=0
OK     https://wp.com  [200]  retries=0
ERROR  https://beian.miit.gov.cn  [HTTP 521]  retries=3
ERROR  https://openai.com  [HTTP 403]  retries=3
<snip>
```
