import http from "k6/http"
import {check, sleep} from "k6";

export const options={
    thresholds:{
        http_req_duration:["p(95)<100"],
        http_req_failed:["rate<0.05"],
    },
};

export default function(){
    const base ="http://localhost:8000";

    const shortenRes = http.post(
        `${base}/shorten`,
        JSON.stringify({original_url:"https://example.com"}),
        {headers: {"Content-Type":"application/json"}}

    );

    check(shortenRes, {
        "shorten status 200": (r) =>r.status===200,
    });
    const slug = shortenRes.json("slug");

    if (slug) {
        const redirectRes = http.get(`${base}/r/${slug}`, {
            redirects: 0,
        });

        check(redirectRes, {
            "redirect status 301": (r) => r.status === 301,
        });
    }

    sleep(1);
}


