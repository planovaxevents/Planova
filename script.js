// ===============================
// STOCK EVENT DATA (UPGRADED + MAP COORDINATES)
// ===============================
const events = [

{
    id: 1,
    title: "NG-ONE THROWBACK NIGHT",
    category: "Clubbing",
    date: "2026-04-27",
    dateLabel: "Sat 15th August",
    dateISO: "2026-08-15T00:13:01",
    time: "21:00 - 03:00",
    location: "NG-ONE Nottingham",
    price: 8,
    priceLabel: "From £8",
    image: "ChatGPT Image Apr 28, 2026, 12_13_05 AM.png",
    description: "A night you won't wanna miss, Dress up and have fun!",

    venue: {
      name: "NG-ONE",
      lat: 52.95487326388578,
      lng: -1.1417604134232073
    },

    venueCapacity: 350,
    ageRestriction: "18+",
    dressCode: "90s - 00s",
    genres: ["Pop", "Hip-Hop", "Rap"],

    ticketAvailability: {
      standard: 325,
      vip: 1,
      vvip: 1
    },

    addons: {
      queue_jump: true,
      drinks_tokens: false,
      afterparty: false,
      merch: false
    },

    promoCodes: {
      "": 0.00
    },

    // ✅ add unique lists (optional but recommended)
    highlights: [
      "",
      "",
      ""
    ],
    whatsIncluded: [
      "",
      "",
      ""
    ],
    venueAmenities: [
      "",
      "",
      ""
    ],

    reviews: [
      { stars: 5, text: "", when: "" },
      { stars: 4, text: "", when: "" }
    ]
  },

  // -----------------------------------------------------------------------------------------------------------------------//

]
// ===============================
// Ticket availability (DEMO using localStorage)
// ===============================
function availabilityKey(eventId) {
  return "planova_availability_" + eventId;
}

function getAvailabilityForEvent(ev) {
  // Start with localStorage copy if present, otherwise use ev.ticketAvailability
  try {
    const stored = localStorage.getItem(availabilityKey(ev.id));
    if (stored) return JSON.parse(stored);
  } catch (e) {}

  // default fallback
  return JSON.parse(JSON.stringify(ev.ticketAvailability || { standard: 0, vip: 0, vvip: 0 }));
}

function saveAvailabilityForEvent(eventId, availabilityObj) {
  try {
    localStorage.setItem(availabilityKey(eventId), JSON.stringify(availabilityObj));
  } catch (e) {}
}

// qtyObj example: { standard: 2, vip: 0, vvip: 1 }
function canPurchaseTickets(ev, qtyObj) {
  const a = getAvailabilityForEvent(ev);

  const s = qtyObj.standard || 0;
  const v = qtyObj.vip || 0;
  const vv = qtyObj.vvip || 0;

  return (
    s >= 0 && v >= 0 && vv >= 0 &&
    a.standard >= s &&
    a.vip >= v &&
    a.vvip >= vv
  );
}

function decrementTickets(ev, qtyObj) {
  const a = getAvailabilityForEvent(ev);

  a.standard -= (qtyObj.standard || 0);
  a.vip -= (qtyObj.vip || 0);
  a.vvip -= (qtyObj.vvip || 0);

  // Never below 0
  a.standard = Math.max(0, a.standard);
  a.vip = Math.max(0, a.vip);
  a.vvip = Math.max(0, a.vvip);

  saveAvailabilityForEvent(ev.id, a);
  return a;
}
// ===============================
// Ticket buttons helper (match your event.html script behaviour)
// ===============================
function setupTicketButtonElement(btn) {
  if (!btn) return;

  var user = null;
  try {
    user = JSON.parse(localStorage.getItem("planova_user") || "null");
  } catch (e) {
    user = null;
  }

  // Clear previous click to prevent stacking
  btn.onclick = null;

  if (!user) {
    btn.textContent = "Create or Sign in to account first!";
    btn.disabled = false;
    btn.style.opacity = "0.85";
    btn.style.cursor = "pointer";

    btn.onclick = function () {
      try { sessionStorage.setItem("planova_redirect_after_auth", window.location.href); } catch (e) {}
      window.location.href = "signin.html";
    };
  } else {
    btn.textContent = "Get tickets";
    btn.disabled = false;
    btn.style.opacity = "1";
    btn.style.cursor = "pointer";

    btn.onclick = function () {
      window.location.href = "gettickets.html";
    };
  }
}

function updateAllTicketButtons() {
  var buttons = [
    document.getElementById("get-tickets-btn-main"),
    document.getElementById("sticky-cta-btn")
  ];

  buttons.forEach(function (btn) {
    setupTicketButtonElement(btn);
  });
}

// ===============================
// Venue map (Leaflet)
// ===============================
function loadVenueMap(lat, lng) {
  const mapContainer = document.getElementById("venue-map");
  if (!mapContainer) return;

  // Reset container (fixes switching events)
  mapContainer.innerHTML = "";

  const map = L.map("venue-map").setView([lat, lng], 15);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "© OpenStreetMap"
  }).addTo(map);

  L.marker([lat, lng]).addTo(map);
}

// ===============================
// RENDER EVENTS INTO SLIDER
// ===============================
function renderEvents(list) {
  const slider = document.getElementById("events-slider");
  if (!slider) return;

  slider.innerHTML = "";

  list.forEach(ev => {
    const card = document.createElement("a");
    card.href = `event.html?id=${ev.id}`;
    card.className = "event-card";

    card.innerHTML = `
      <img src="${ev.image}" />
      <div class="event-card-body">
        <span class="badge">${ev.category}</span>
        <h3 class="event-title">${ev.title}</h3>
        <p class="event-meta">${ev.dateLabel} · ${ev.time} · ${ev.location}</p>
        <div class="event-footer">
          <span class="event-price">${ev.priceLabel}</span>
          <span class="event-cta">View tickets →</span>
        </div>
      </div>
    `;

    // Store event for event.html + gettickets.html
    card.addEventListener("click", () => {
      localStorage.setItem("selected_event", JSON.stringify(ev));
    });

    slider.appendChild(card);
  });
}

// ===============================
// SORTING
// ===============================
function sortEvents(list, mode) {
  const arr = [...list];
  if (mode === "price-asc") arr.sort((a, b) => a.price - b.price);
  if (mode === "price-desc") arr.sort((a, b) => b.price - a.price);
  if (mode === "date") arr.sort((a, b) => new Date(a.date) - new Date(b.date));
  return arr;
}

// ===============================
// SEARCH
// ===============================
function setupSearch() {
  const form = document.getElementById("hero-search");
  if (!form) return;

  form.addEventListener("submit", e => {
    e.preventDefault();

    const q = document.getElementById("search-input").value.toLowerCase();
    const loc = document.getElementById("search-location").value.toLowerCase();

    const results = events
      .filter(ev =>
        ev.title.toLowerCase().includes(q) ||
        ev.category.toLowerCase().includes(q) ||
        ev.location.toLowerCase().includes(q)
      )
      .filter(ev => loc === "" || ev.location.toLowerCase().includes(loc));

    renderEvents(results);
  });
}

// ===============================
// DATE FILTERS
// ===============================
function setupDateFilters() {
  const dateFilters = document.getElementById("date-filters");
  if (!dateFilters) return;

  dateFilters.addEventListener("click", e => {
    const btn = e.target.closest("button");
    if (!btn) return;

    document.querySelectorAll("#date-filters button").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");

    renderEvents(filterByDate(btn.dataset.range));
  });
}

// ===============================
// EVENT DETAIL LOADER
// ✅ now also pushes unique lists into selected_event for event.html
// ===============================
function loadEventDetail() {
  if (!window.location.pathname.includes("event.html")) return;

  const params = new URLSearchParams(window.location.search);
  const id = parseInt(params.get("id"));
  const ev = events.find(e => e.id === id);
  if (!ev) return;

  // Store event for tickets page + event.html script (includes unique lists)
  localStorage.setItem("selected_event", JSON.stringify(ev));

  // HERO SECTION
  document.getElementById("event-title").textContent = ev.title;
  document.getElementById("badge-category").textContent = ev.category;
  document.getElementById("badge-age").textContent = ev.ageRestriction;
  document.getElementById("badge-dress").textContent = ev.dressCode;

  document.getElementById("event-meta").textContent = `${ev.dateLabel} · ${ev.time} · ${ev.location}`;
  document.getElementById("event-submeta").textContent = `${ev.venueCapacity} capacity`;
  document.getElementById("event-image").src = ev.image;

  // ABOUT SECTION
  document.getElementById("event-description").textContent = ev.description;
  document.getElementById("stat-capacity").textContent = ev.venueCapacity;
  document.getElementById("stat-genres").textContent = ev.genres.join(", ");
  document.getElementById("stat-age").textContent = ev.ageRestriction;
  document.getElementById("stat-dress").textContent = ev.dressCode;

  // TICKET CARD
  document.getElementById("ticket-price").textContent = ev.priceLabel;
  document.getElementById("ticket-note").textContent = "Prices may vary by ticket type";

  // STICKY CTA
  document.getElementById("sticky-cta-title").textContent = ev.title;
  document.getElementById("sticky-cta-price").textContent = ev.priceLabel;

  // Venue map
  if (ev.venue && ev.venue.lat && ev.venue.lng) {
    loadVenueMap(ev.venue.lat, ev.venue.lng);
  }

  // Dynamic background image
  document.body.style.background = `url('${ev.image}') no-repeat center center fixed`;
  document.body.style.backgroundSize = "cover";

  // ✅ Ticket buttons on event page (main + sticky)
  updateAllTicketButtons();
}

// ===============================
// DATE FILTER CORE
// ===============================
function filterByDate(range) {
  const today = new Date();
  const eventsCopy = [...events];

  if (range === "all") return eventsCopy;

  if (range === "today") {
    return eventsCopy.filter(ev => {
      const evDate = new Date(ev.date);
      return evDate.toDateString() === today.toDateString();
    });
  }

  if (range === "weekend") {
    const day = today.getDay(); // 0 = Sun, 6 = Sat
    const saturday = new Date(today);
    const sunday = new Date(today);

    saturday.setDate(today.getDate() + (6 - day));
    sunday.setDate(saturday.getDate() + 1);

    return eventsCopy.filter(ev => {
      const evDate = new Date(ev.date);
      return evDate >= saturday && evDate <= sunday;
    });
  }

  if (range === "week") {
    const nextWeek = new Date(today);
    nextWeek.setDate(today.getDate() + 7);

    return eventsCopy.filter(ev => {
      const evDate = new Date(ev.date);
      return evDate >= today && evDate <= nextWeek;
    });
  }

  return eventsCopy;
}

// ===============================
// INITIALISE
// ===============================
window.addEventListener("DOMContentLoaded", () => {
  // HOME PAGE
  if (document.getElementById("events-slider")) {
    renderEvents(events);
    setupSearch();

    const sortSelect = document.getElementById("sort-select");
    if (sortSelect) {
      sortSelect.addEventListener("change", e => {
        renderEvents(sortEvents(events, e.target.value));
      });
    }

    setupDateFilters();

    document.querySelectorAll(".hero-tags button")?.forEach(btn => {
      btn.addEventListener("click", () => {
        const tag = btn.dataset.tag;
        renderEvents(events.filter(ev => ev.category === tag));
      });
    });
  }

  // EVENT PAGE
  loadEventDetail();
});

// ===============================
// PASSWORD TOGGLE
// ===============================
document.querySelectorAll(".toggle-password")?.forEach(btn => {
  btn.addEventListener("click", () => {
    const input = btn.previousElementSibling;
    input.type = input.type === "password" ? "text" : "password";
  });
});

// ===============================
// COPY LINK BUTTON
// ===============================
document.querySelectorAll(".copy-link")?.forEach(btn => {
  btn.addEventListener("click", () => {
    navigator.clipboard.writeText(window.location.href);
    btn.textContent = "Copied!";
    setTimeout(() => (btn.textContent = "Copy link"), 1500);
  });
});

// ===============================
// TICKET MODAL
// ===============================
const ticketBtn = document.getElementById("open-ticket-modal");
const ticketModal = document.getElementById("ticket-modal");
const closeModal = document.getElementById("close-modal");

if (ticketBtn && ticketModal) {
  ticketBtn.addEventListener("click", () => {
    ticketModal.classList.add("show");
  });
}

if (closeModal && ticketModal) {
  closeModal.addEventListener("click", () => {
    ticketModal.classList.remove("show");
  });
}

// ===============================
// SLIDER ARROWS
// ===============================
const sliderEl = document.getElementById("events-slider");
const btnLeft = document.getElementById("slide-left");
const btnRight = document.getElementById("slide-right");

if (sliderEl && btnLeft && btnRight) {
  btnLeft.addEventListener("click", () => {
    sliderEl.scrollBy({ left: -300, behavior: "smooth" });
  });

  btnRight.addEventListener("click", () => {
    sliderEl.scrollBy({ left: 300, behavior: "smooth" });
  });
}