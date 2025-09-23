var metas = document.getElementsByTagName("meta");
var mediaURL = "";
for (var i=0; i<metas.length; i++) {
    if (metas[i].getAttribute("property") === "og:video") {
        mediaURL = metas[i].getAttribute("content");
        break;
    }
    if (metas[i].getAttribute("property") === "og:image") {
        mediaURL = metas[i].getAttribute("content");
    }
}
completion(mediaURL);