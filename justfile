default:
	just --list
new:
	#!/usr/bin/env bash
	set -euxo pipefail
	i="$(printf "%02d" "$(exa -D | rg "\d{2}" | wc -l)")"
	mkdir $i
	touch $i/README.md
