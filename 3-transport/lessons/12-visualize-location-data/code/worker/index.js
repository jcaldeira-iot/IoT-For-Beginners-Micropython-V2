export default {
    async fetch(request, env) {
        const url = new URL(request.url);

        if (request.method === "POST" && url.pathname === "/telemetry") {
            return handleTelemetry(request, env);
        }

        const gpsMatch = url.pathname.match(/^\/gps\/([^/]+)$/);
        if (request.method === "GET" && gpsMatch) {
            return handleGps(decodeURIComponent(gpsMatch[1]), env);
        }

        return new Response("Not found", { status: 404 });
    },
};

// A device sends telemetry and the service confirms that it was received
async function handleTelemetry(request, env) {
    const deviceId = request.headers.get("x-device-id");
    const deviceKey = request.headers.get("x-api-key");
    if (!deviceId || !deviceKey) {
        return new Response("Unauthorized", { status: 401 });
    }

    // Only registered devices with the right secret key are accepted
    const registeredKey = await env.DEVICE_STATE.get(`device:${deviceId}`);
    if (registeredKey === null || registeredKey !== deviceKey) {
        return new Response("Unauthorized", { status: 401 });
    }

    let telemetry;
    try {
        telemetry = await request.json();
    } catch {
        return new Response("Invalid JSON", { status: 400 });
    }

    const gps = telemetry.gps;
    if (!gps || typeof gps.lat !== "number" || typeof gps.lon !== "number") {
        return new Response("gps.lat and gps.lon must be numbers", { status: 400 });
    }

    console.log("Worker processed an event: " + JSON.stringify({ gps }));

    const timestamp = new Date().toISOString();
    const key = `${deviceId}/${timestamp}-${crypto.randomUUID()}.json`;

    const body = {
        device_id: deviceId,
        timestamp,
        gps,
    };

    console.log(`Writing key ${key} - ${JSON.stringify(body)}`);
    await env.GPS_DATA.put(key, JSON.stringify(body));

    return Response.json({ status: "received" });
}

// A web page asks for the most recent GPS readings of a device
const MAX_POINTS = 40;

const corsHeaders = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
};

async function handleGps(deviceId, env) {
    // The keys start with the time, so they are listed oldest first
    const list = await env.GPS_DATA.list({ prefix: `${deviceId}/` });
    const keys = list.keys.slice(-MAX_POINTS);

    const readings = await Promise.all(
        keys.map((key) => env.GPS_DATA.get(key.name, "json"))
    );

    const features = readings
        .filter((reading) => reading && reading.gps)
        .map((reading) => ({
            type: "Feature",
            properties: {
                device_id: reading.device_id,
                timestamp: reading.timestamp,
            },
            geometry: {
                type: "Point",
                coordinates: [reading.gps.lon, reading.gps.lat],
            },
        }));

    return Response.json(
        { type: "FeatureCollection", features },
        { headers: corsHeaders }
    );
}
