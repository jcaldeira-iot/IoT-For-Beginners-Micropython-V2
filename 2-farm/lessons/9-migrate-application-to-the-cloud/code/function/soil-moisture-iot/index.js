export default {
      async fetch(request, env) {
        const url = new URL(request.url);

        if (request.method === "POST" && url.pathname === "/telemetry") {
          return handleTelemetry(request, env);
        }
        return new Response("Not found", { status: 404 });
      },
    };

    // A device sends telemetry and receives a command in the reply
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

      const soilMoisture = telemetry.soil_moisture;
      if (typeof soilMoisture !== "number") {
        return new Response("soil_moisture must be a number", { status: 400 });
      }

      // Decide if the plant needs watering
      const command = soilMoisture > THRESHOLD ? "relay_on" : "relay_off";

      console.log(JSON.stringify({ device: deviceId, soil_moisture: soilMoisture, command }));

      return Response.json({ command });
    }
