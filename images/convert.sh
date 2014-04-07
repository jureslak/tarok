for f in *.jpg; do
    echo $f
    convert -resize 100x180\! $f "${f::-4}.ppm";
done
