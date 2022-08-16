# Export shotwell tags to digikam

# Rational

Shotwell can write the tags and rating into jpg images, but it cannot write such metadata into movies.
the *.xmp files with the same base name as the images and movies.

Digikam does read these*.xmp files on import and therefore also imports the tags and rating.

## Adjust these lines in the file ExportShotwellXMP.py to yours needs

PrunePath="/home/xxxxx/"

ShotwellDBDir=".shotwell/data/"

# Caution

Use it at your own risks.

Since I do not need this code anymore, there will be not further improvements from my side.
Feel free to fork and adjust to your needs.
