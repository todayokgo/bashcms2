#!/bin/bash -euxv
source "$(dirname $0)/conf"
exec 2> "$logdir/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"
set -o pipefail

trap 'rm -f $tmp-*' EXIT

### VARIABLES ###
tmp=/tmp/$$
dir="$(tr -dc 'a-zA-Z0-9_=' <<< ${QUERY_STRING} | sed 's;=;s/;')"
md="$contentsdir/$dir/main.md"
[ -f "$md" ]

### MAKE HTML ###
cat << FIN > $tmp-meta.yaml
---
created_time: '$(date -f - < $datadir/$dir/created_time)'
modified_time: '$(date -f - < $datadir/$dir/modified_time)'
title: '$(cat "$datadir/$dir/title")'
nav: '$(cat "$datadir/$dir/nav")'
---
FIN

### OUTPUT ###
pandoc --template="$viewdir/template.html" \
	-f markdown_github+yaml_metadata_block "$md" "$tmp-meta.yaml" |
sed -r "/:\/\/|\"\//!s;<(img src|a href)=\";&/$dir/;" |
sed "s;/$dir/#;#;g"
