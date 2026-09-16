#!/usr/bin/env bash
# Report which NSI datasets under a scratch dir are incomplete.
# Usage: check_datasets.sh [SCRATCH_DIR] [DEPOT_DIR]
set -uo pipefail
SCRATCH="${1:-/home/li5273/Desktop/data}"
DEPOT="${2:-/depot/bouman/data/Lilly}"

printf '%-38s %10s %10s %6s %7s %7s  %s\n' DATASET TGZ EXTRACTED RATIO TIFS EXPECT STATUS
for tgz in "$SCRATCH"/*.tgz "$SCRATCH"/*.tar.gz "$SCRATCH"/*.tar; do
    [ -e "$tgz" ] || continue
    base=$(basename "$tgz"); name="${base%.tgz}"; name="${name%.tar.gz}"; name="${name%.tar}"
    dir="$SCRATCH/$name"
    status=""

    # 1. tarball truncated relative to the depot original?
    depot=$(find "$DEPOT" -maxdepth 2 -name "$base" -print -quit 2>/dev/null)
    tsz=$(stat -Lc%s "$tgz")
    if [ -n "$depot" ]; then
        dsz=$(stat -Lc%s "$depot")
        [ "$tsz" -ne "$dsz" ] && status="TRUNCATED_TARBALL"
    fi

    # 2. extracted tree missing, or smaller than the compressed tarball
    #    (gzip never expands, so extracted < tarball means a partial tree)
    if [ ! -d "$dir" ]; then
        ebytes=0; status="${status:+$status,}NOT_EXTRACTED"
    else
        ebytes=$(du -sb "$dir" 2>/dev/null | cut -f1)
        if [ -z "$status" ] && [ "$ebytes" -lt "$tsz" ]; then status="PARTIAL_EXTRACT"; fi
    fi
    ratio=$(awk -v a="$ebytes" -v b="$tsz" 'BEGIN{printf "%.2f", (b>0? a/b : 0)}')

    # 3. exact count: .nsipro declares the projection count; compare to .tif on disk
    tifs=NA; expect=NA
    if [ -d "$dir" ]; then
        tifs=$(find "$dir" -name '*.tif' 2>/dev/null | wc -l)
        expect=$(grep -ho '<Number of projections>[0-9]*' "$dir"/*.nsipro 2>/dev/null |
                 head -1 | tr -dc '0-9')
        [ -z "$expect" ] && expect=NA
        if [ "$expect" != NA ] && [ "$tifs" -lt "$expect" ]; then
            case "$status" in *MISSING_VIEWS*) ;; *) status="${status:+$status,}MISSING_VIEWS";; esac
        fi
    fi

    printf '%-38s %9.2fG %9.2fG %6s %7s %7s  %s\n' \
        "$name" "$(awk -v v="$tsz" 'BEGIN{print v/1073741824}')" \
        "$(awk -v v="$ebytes" 'BEGIN{print v/1073741824}')" "$ratio" "$tifs" "$expect" "${status:-OK}"
done
