// Modify the behavior of firefox to better suit using it as tabless
// webpage viewer as firefox-show.

// Prefer opening in new windows rather than new tabs
user_pref("browser.link.open_newwindow", 2);

// Don't store browsing history
user_pref("browser.privatebrowsing.autostart", true);

// Don't show privacy notice on first run
user_pref("toolkit.telemetry.reportingpolicy.firstRun", false);

// Use a cleaned up version of the new tab page as the home page.
user_pref("browser.startup.homepage", "about:newtab");
user_pref("browser.startup.homepage_override.mstone", "ignore");
user_pref("browser.newtabpage.activity-stream.feeds.section.highlights", false);
user_pref("browser.newtabpage.activity-stream.feeds.section.topstories", false);
user_pref("browser.newtabpage.activity-stream.feeds.topsites", false);
