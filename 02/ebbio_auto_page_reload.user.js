// ==UserScript==
// @name        ebb.io 自動重新加載
// @namespace   Violentmonkey Scripts
// @match       https://ebb.io/*
// @grant       none
// @version     1.0
// @author      CcydtN
// @description Add button to each episode that helps reload page automatically.
// @require https://cdn.jsdelivr.net/npm/jquery@3/dist/jquery.min.js
// ==/UserScript==

const flag_name = "reload";
function set_flag(val) {
	sessionStorage.setItem(flag_name, val);
}
function get_flag() {
	return sessionStorage.getItem(flag_name) == "true";
}

const config = {
	attributes: false,
	childList: true,
	characterData: false,
	subtree: true,
};

// Entry point
$(document).ready(() => {
	"use strict";
	const observer = new MutationObserver(page_modify);
	observer.observe(document.body, config);
});

// Trigger multiple time
function page_modify(list, observer) {
	// This function is going to modify the page which trigger the observer recursively
	// dissconect to prevent that
	observer.disconnect();

	add_button_for_each_episode();

	let flag = get_flag();
	// console.log({toggle});
	if (!flag) {
		observer.observe(document.body, config);
		return;
	}

	const isError = $(".error-message").length != 0;
	if (isError) {
		fail_handle();
		observer.observe(document.body, config);
		return;
	}

	const isLoaded = $("video").first().attr("src");
	if (isLoaded) {
		console.log("Video ready, Stop reloading");
		set_flag(false);
	}

	observer.observe(document.body, config);
}

function add_button_for_each_episode() {
	$("div.actions").each(function (index, element) {
		// skip if already append
		if ($(this).children().length != 1) {
			return;
		}

		const clone = $(this).children().first().clone();
		let href = clone.attr("href");
		let idx = href.lastIndexOf("=");
		let episode = href.substring(idx + 1);

		clone.on("click", (event) => {
			console.log("Start reloading");
			event.preventDefault();
			set_flag(true);
			updateWatchHistory(episode);
			location.reload();
		});

		clone.attr("href", "javascript:void(0)");
		clone.text("(・∀・)");

		$(this).append(clone);
	});
}

function fail_handle() {
	// check for a div
	// if exist, it means fail_handle had run already and no need to run again.
	if ($(".error-message div div").length == 0) {
		return;
	}

	delay = 5;
	delay_ns = delay * 1000;
	console.log("Set timer " + delay + "s");

	// add reload countdown and cancel button to error message
	let counter = $("<a>", { text: delay });
	let content = $("<a>", { text: " 秒後重試... " });
	let cancel = $("<a>", { href: "javascript:void(0)", text: "取消" });

	let message = $("<div>");
	message.append($("<br>"));
	message.append(counter);
	message.append(content);
	message.append(cancel);

	$(".error-message div").append(message);

	var idxs = [];
	idxs.push(
		setTimeout(() => {
			location.reload();
		}, delay_ns),
	); // reload timeout

	for (var i = 1; i <= 5; i += 1) {
		let idx = setTimeout(() => {
			counter.text(counter.text() - 1);
		}, 1000 * i);
		idxs.push(idx);
	}

	cancel.on("click", (event) => {
		console.log("Stop reloading");
		set_flag(false);
		for (var idx of idxs) {
			clearTimeout(idx);
		}
		message.remove();
	});
}

function updateWatchHistory(episode) {
	const current_url = window.location.href;
	const api_url = "https://ebb.io/_/update_watch_history";

	const seasonId = current_url.substring(current_url.lastIndexOf("x") + 1);
	const title = '"' + episode + '"';
	var data = new FormData();

	data.set("seasonId", seasonId);
	data.set("title", title);
	data.set("time", 0);
	console.log({ data });

	var xhttp = new XMLHttpRequest();
	xhttp.open("POST", api_url, false);
	xhttp.send(data);
}
