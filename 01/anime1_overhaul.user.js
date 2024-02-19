// ==UserScript==
// @name        Anime1 overhaul
// @namespace   Violentmonkey Scripts
// @match       http*://anime1.me/*
// @match       http*://anime1.pw/*
// @exclude     http*://anime1.me/
// @exclude     http*://anime1.pw/
// @grant       none
// @version     1.0
// @author      CcydtN
// @description It currently do two things. One, set player to full page width (and remove the side bar). Second, disable volume change on scroll.
// ==/UserScript==

// Entry point
$(document).ready(() => {
	set_content_full_width();
	disable_volume_change_on_scroll();
});

function set_content_full_width() {
	$("#primary").css("width", "100%");
	$(".vjscontainer").css("height", "100%");
	$(".vjscontainer").css("max-width", "100%");
	// remove side bar
	$("#secondary").css("display", "none");
}

function disable_volume_change_on_scroll() {
	$(".vjscontainer")
		.children()
		.each((id, element) => {
			// Volume change is trigger by "mousewheel" event
			// Disable the event is impossible, because the function reference cannot be obtain. Check "removeEventListener"
			//
			// But "mousewheel" is deprecated, "wheel" is suggested.
			// In vivaldi, execution of "mousewheel" can be prevent by adding handler to "wheel".
			// I assume all chromium-base browser have same behaviour
			//
			// Can be tested by the following code
			// $(element).on("wheel", ()=>{console.log("wheel")})
			// $(element).on("mousewheel", ()=>{console.log("mousewheel")})
			$(element).on("wheel", () => {});
		});
}
