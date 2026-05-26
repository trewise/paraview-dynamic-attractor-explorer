#!/usr/bin/env bash
set -e

export PYTHONPATH=/usr/lib/python3/dist-packages:$PYTHONPATH
export LIBGL_ALWAYS_SOFTWARE=1
export MESA_GL_VERSION_OVERRIDE=3.3

FRAMES=120
FPS=30

ATTRACTORS=(
  lorenz
  rossler
  thomas
  aizawa
  chen
  dadras
  four_wing
  halvorsen
  sprott_a
  sprott_b
  sprott_c
)

for NAME in "${ATTRACTORS[@]}"
do
  echo
  echo "================================================="
  echo "FLYTHROUGH: ${NAME}"
  echo "================================================="

  DATASET="datasets/attractors/${NAME}/${NAME}_trajectory.vtp"
  FRAME_DIR="outputs/flythrough_frames/${NAME}"
  MP4="outputs/animations/${NAME}_flythrough.mp4"
  GIF="outputs/animations/${NAME}_flythrough.gif"

  mkdir -p "$FRAME_DIR"

  if [ ! -f "$DATASET" ]; then
    echo "SKIP: missing dataset $DATASET"
    continue
  fi

  rm -f "$FRAME_DIR"/frame_*.png

  for i in $(seq 0 $((FRAMES - 1)))
  do
    FRAME=$(printf "%04d" "$i")
    echo "${NAME}: frame ${FRAME}/${FRAMES}"

    xvfb-run -a -s "-screen 0 1200x800x24" \
      /usr/bin/pvpython \
      paraview/python_scripts/render_animation.py \
      "$DATASET" \
      "$FRAME_DIR/frame_${FRAME}.png" \
      flythrough \
      "$i" \
      "$FRAMES"
  done

  COUNT=$(find "$FRAME_DIR" -name "frame_*.png" | wc -l)

  echo "Frame count for ${NAME}: ${COUNT}"

  if [ "$COUNT" -ne "$FRAMES" ]; then
    echo "ERROR: ${NAME} generated ${COUNT}/${FRAMES} frames"
    exit 1
  fi

  ffmpeg -y \
    -framerate "$FPS" \
    -i "$FRAME_DIR/frame_%04d.png" \
    -c:v libx264 \
    -pix_fmt yuv420p \
    "$MP4"

  ffmpeg -y \
    -i "$MP4" \
    -vf "fps=15,scale=800:-1:flags=lanczos" \
    "$GIF"

  cp "$MP4" "portfolio/videos/${NAME}_flythrough.mp4"
  cp "$GIF" "portfolio/videos/${NAME}_flythrough.gif"

  echo "DONE: ${NAME}"
done

echo
echo "================================================="
echo "ALL FLYTHROUGHS COMPLETE"
echo "================================================="

ls -lh outputs/animations
