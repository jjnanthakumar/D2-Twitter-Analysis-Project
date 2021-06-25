const URL = "https://api.heroku.com/apps/nlptweets/releases"
const header = {
    Accept: "application/vnd.heroku+json; version=3",
    Authorization: "Bearer <heroku access token>"
}
fetch(URL, { headers: header })
    .then(res => res.json())
    .then(res => {
        let lastone = res.pop()
        let updated_at = new Date(lastone.updated_at).toLocaleString()
        // window.data.version = lastone.version
        $('#pageupd').html(updated_at)
    });