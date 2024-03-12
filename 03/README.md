## Motivation
I read some fourm post (few years ago), saying that he practice english speech by mimiking the way of Ted Talk speakers. 

I think getting a speech script can help me do the same practice, so I write the following code to help me get the closed captions and convert it in to a script.

## Usage
```sh
just download [url]
```

## Main goal
- Download the closed captions from TED talk youtube video.
- Split paragraph into lines, make it easier to follow.

## How it done
1. Use `yt-dlp` to download the english subtitle in `.srt` format. [\[srt foramt wiki\]](https://en.wikipedia.org/wiki/SubRip)
2. Use natural language processing (NLP) to split the sentence.

## Why NLP
I don't want the script read likes books/new, having sentence break in the middle and continue on the next line.

It should read like text on teleprompter. Like having one sentence in one line, provide enough hint for speech and easy to follow.

My first idea is REGEX, but there are too much cases that might need to takecare. Here are some example:
- it can be end with `.`, `?`, `!`, etc.
- it can be a quote, which surround by `'`, `"`
- `.` can be appear in the sentence, like `...`, abbreviation ("Sept." for "September").
- the subtitle didn't use a footstop, it jump from one sentence to another.
- etc.

I don't think writing REGEX for splitting stentance is feasible. It probably not going to work.

The second solution came up in my mind is NLP. So I try it and the result is promising.

