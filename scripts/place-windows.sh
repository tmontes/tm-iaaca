#!/bin/bash

VSCODE_X=32
VSCODE_Y=50
VSCODE_W=1216
VSCODE_H=760

PDFL_X=32
PDFL_Y=50
PDFL_W=1216
PDFL_H=760


VSCODE_ID=$(
    yabai -m query --windows |
    jq -r '.[] |
        select(
          ((.title // "")       | ascii_downcase | contains("trust-me-i-am-a-cert-auth"))
        ) |
        .id
    '
)
PDFL_ID=$(
    yabai -m query --windows |
    jq -r '.[] |
        select(
          ((.app // .name // "") | ascii_downcase | contains("pdfless"))
        ) |
        .id
    '
)

yabai -m window "${VSCODE_ID}" --move abs:${VSCODE_X}:${VSCODE_Y}
yabai -m window "${VSCODE_ID}" --resize abs:${VSCODE_W}:${VSCODE_H}

yabai -m window "${PDFL_ID}" --move abs:${PDFL_X}:${PDFL_Y}
yabai -m window "${PDFL_ID}" --resize abs:${PDFL_W}:${PDFL_H}


