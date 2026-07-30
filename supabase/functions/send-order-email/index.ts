import { serve } from "https://deno.land/std@0.190.0/http/server.ts";

const RESEND_API_KEY = Deno.env.get("RESEND_API_KEY");
const TO_EMAIL = "mjolnariclan@gmail.com";

serve(async (req) => {
  try {
    const order = await req.json();

    const html = `
      <h2>New Order Received</h2>
      <p><strong>Name:</strong> ${order.name}</p>
      <p><strong>Email:</strong> ${order.email}</p>
      <p><strong>Phone:</strong> ${order.phone || "N/A"}</p>
      <p><strong>Service:</strong> ${order.service}</p>
      <p><strong>Deadline:</strong> ${order.deadline || "N/A"}</p>
      <p><strong>Notes:</strong> ${order.notes || "N/A"}</p>
      <p><strong>Source Link:</strong> ${order.source_link || "N/A"}</p>
      <p><strong>Colors:</strong> ${(order.selected_colors || []).join(", ")}</p>
      <p><strong>Files:</strong> ${(order.file_names || []).join(", ")}</p>
    `;

    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${RESEND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: "Orders <onboarding@resend.dev>",
        to: [TO_EMAIL],
        subject: `New Order from ${order.name}`,
        html,
      }),
    });

    if (!res.ok) {
      const errText = await res.text();
      console.error("Resend error:", errText);
      return new Response(JSON.stringify({ error: errText }), { status: 500 });
    }

    const data = await res.json();
    return new Response(JSON.stringify(data), { status: 200 });
  } catch (err) {
    console.error(err);
    return new Response(JSON.stringify({ error: String(err) }), { status: 500 });
  }
});