set -e

npm run build

cd dist

git init
git add -A
git commit -m 'deploying'

git push -f https://github.com/ericskelly/spotify-playlist-merger.git master:gh-pages
