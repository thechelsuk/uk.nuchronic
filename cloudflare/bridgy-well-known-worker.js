export default {
    async fetch(request) {
        const url = new URL(request.url);

        if (
            url.pathname === "/.well-known/host-meta" ||
            url.pathname === "/.well-known/webfinger"
        ) {
            return Response.redirect(
                `https://fed.brid.gy${url.pathname}${url.search}`,
                302,
            );
        }

        return fetch(request);
    },
};
