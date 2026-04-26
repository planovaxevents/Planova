// ===============================
// STOCK EVENT DATA (UPGRADED + MAP COORDINATES)
// ===============================
const events = [
  {
    id: 1,
    title: "NGONE 90's - 00's Throwback",
    category: "Clubbing",
    date: "2026-05-02",
    dateLabel: "Fri 2 May",
    dateISO: "2026-05-02T22:00:00",
    time: "22:00–04:00",
    location: "Nottingham",
    price: 12,
    priceLabel: "From £12.00",
    image: "https://images.pexels.com/photos/1190297/pexels-photo-1190297.jpeg",
    description: "A high‑energy night of house and techno with immersive lighting and top DJs.",

    venue: {
      name: "NG-One Nottingham",
      lat: 52.95487222627411,
      lng: -1.1417576293234528
    },

    venueCapacity: 900,
    ageRestriction: "18+",
    dressCode: "Smart casual",
    genres: ["House", "Techno", "Throwbacks"],

    ticketAvailability: {
      standard: 150,
      vip: 40,
      vvip: 10
    },

    addons: {
      queue_jump: true,
      drinks_tokens: true,
      afterparty: false,
      merch: true
    },

    promoCodes: {
      "NGONE10": 0.10
    },

    reviews: [
      { stars: 5, text: "Unreal throwback vibes!", when: "Last month" },
      { stars: 4, text: "DJ set was insane.", when: "2 weeks ago" }
    ]
  },



// -----------------------------------------------------------------------------------------------------------------------//
  


  {
  id: 2,
  title: "Cell - Fiesta Fuego",
  category: "Clubbing", // or Live Music, etc.
  date: "2026-06-10",
  dateLabel: "Sat 10 Jun",
  dateISO: "2026-06-10T18:00:00",
  time: "18:00–23:00",
  location: "Nottingham",
  price: 15,
  priceLabel: "From £15.00",
  image: "https://images.pexels.com/photos/167404/pexels-photo-167404.jpeg",
  description: "Live bands, cocktails and sunset views over the city.",

  venue: {
    name: "Cell Nottingham",
    lat: 52.953200,
    lng: -1.150900
  },

  venueCapacity: 350,
  ageRestriction: "18+",
  dressCode: "Casual / Summer",
  genres: ["Latin", "Live Bands", "Summer Vibes"],

  ticketAvailability: {
    standard: 80,
    vip: 20,
    vvip: 0
  },

  addons: {
    queue_jump: false,
    drinks_tokens: true,
    afterparty: false,
    merch: false
  },

  promoCodes: {},

  reviews: [
    { stars: 5, text: "Amazing atmosphere!", when: "3 weeks ago" }
  ],

  // 🔥 NEW: per‑event content
  highlights: [
    "Live Latin bands all evening",
    "Rooftop sunset views over Nottingham",
    "Signature rum cocktails and summer décor"
  ],

  whatsIncluded: [
    "Standard entry to Cell Nottingham",
    "Access to all live band performances",
    "Cloakroom available on site (extra charge)"
  ],

  venueAmenities: [
    "Rooftop terrace with city views",
    "Multiple bars and cocktail stations",
    "Outdoor heaters and covered seating",
    "Nearby tram and bus connections"
  ]
},


  // -----------------------------------------------------------------------------------------------------------------------//
  


  {
    id: 3,
    title: "Rock City - Asian Night Out",
    category: "Festival",
    date: "2026-07-21",
    dateLabel: "Sun 21 Jul",
    dateISO: "2026-07-21T12:00:00",
    time: "12:00–23:00",
    location: "Nottingham",
    price: 35,
    priceLabel: "From £35.00",
    image: "https://images.pexels.com/photos/1190298/pexels-photo-1190298.jpeg",
    description: "A full‑day outdoor festival featuring bassline, DnB and UKG artists.",

    venue: {
      name: "Rock City Nottingham",
      lat: 52.956600,
      lng: -1.154900
    },

    venueCapacity: 6000,
    ageRestriction: "16+",
    dressCode: "Festival wear",
    genres: ["Bassline", "DnB", "UKG"],

    ticketAvailability: {
      standard: 1200,
      vip: 300,
      vvip: 60
    },

    addons: {
      queue_jump: true,
      drinks_tokens: true,
      afterparty: true,
      merch: true
    },

    promoCodes: {
      "FEST15": 0.15
    },

    reviews: [
      { stars: 5, text: "Massive lineup!", when: "1 month ago" },
      { stars: 4, text: "VIP lounge was worth it.", when: "2 weeks ago" }
    ]
  },



  // -----------------------------------------------------------------------------------------------------------------------//
  


  {
    id: 4,
    title: "Mojos - Students Off School",
    category: "Student Night",
    date: "2026-04-28",
    dateLabel: "Wed 28 Apr",
    dateISO: "2026-04-28T22:00:00",
    time: "22:00–03:00",
    location: "Nottingham",
    price: 5,
    priceLabel: "From £5.00",
    image: "https://images.pexels.com/photos/2747441/pexels-photo-2747441.jpeg",
    description: "A night of 2000s and 2010s throwback hits for students.",

    venue: {
      name: "Mojos Nottingham",
      lat: 52.953900,
      lng: -1.152300
    },

    venueCapacity: 1100,
    ageRestriction: "18+ (Student ID required)",
    dressCode: "Anything goes",
    genres: ["Throwbacks", "RnB", "Chart"],

    ticketAvailability: {
      standard: 300,
      vip: 40,
      vvip: 0
    },

    addons: {
      queue_jump: true,
      drinks_tokens: false,
      afterparty: false,
      merch: false
    },

    promoCodes: {
      "STUDENT5": 0.05
    },

    reviews: [
      { stars: 5, text: "Best student night in the city!", when: "Last week" }
    ]
  },



  // -----------------------------------------------------------------------------------------------------------------------//
  


  {
    id: 5,
    title: "INK - Tech House Takeover",
    category: "Clubbing",
    date: "2026-05-18",
    dateLabel: "Sat 18 May",
    dateISO: "2026-05-18T22:00:00",
    time: "22:00–05:00",
    location: "London",
    price: 22,
    priceLabel: "From £22.00",
    image: "https://images.pexels.com/photos/3586968/pexels-photo-3586968.jpeg",
    description: "A massive tech‑house takeover in the heart of London featuring top UK DJs.",

    venue: {
      name: "INK London",
      lat: 51.509865,
      lng: -0.118092
    },

    venueCapacity: 1500,
    ageRestriction: "18+",
    dressCode: "Smart / Clubwear",
    genres: ["Tech House", "House"],

    ticketAvailability: {
      standard: 200,
      vip: 60,
      vvip: 20
    },

    addons: {
      queue_jump: true,
      drinks_tokens: true,
      afterparty: true,
      merch: true
    },

    promoCodes: {
      "INK20": 0.20
    },

    reviews: [
      { stars: 5, text: "London energy was unreal!", when: "2 weeks ago" }
    ]
  },



  // -----------------------------------------------------------------------------------------------------------------------//
  


  {
    id: 6,
    title: "Manchester Indie Live – Northern Sound",
    category: "Live Music",
    date: "2026-06-14",
    dateLabel: "Sun 14 Jun",
    dateISO: "2026-06-14T19:00:00",
    time: "19:00–23:30",
    location: "Manchester",
    price: 18,
    priceLabel: "From £18.00",
    image: "https://images.pexels.com/photos/1763075/pexels-photo-1763075.jpeg",
    description: "Manchester’s biggest indie night returns with live bands and local talent.",

    venue: {
      name: "Manchester Academy",
      lat: 53.467200,
      lng: -2.233400
    },

    venueCapacity: 500,
    ageRestriction: "18+",
    dressCode: "Casual",
    genres: ["Indie", "Rock"],

    ticketAvailability: {
      standard: 120,
      vip: 20,
      vvip: 0
    },

    addons: {
      queue_jump: false,
      drinks_tokens: true,
      afterparty: false,
      merch: false
    },

    promoCodes: {},

    reviews: [
      { stars: 5, text: "Incredible live bands!", when: "Last month" }
    ]
  }
];



// -----------------------------------------------------------------------------------------------------------------------//
  

















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

    // ⭐ Store event for event.html + gettickets.html
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

    const results = events.filter(ev =>
      ev.title.toLowerCase().includes(q) ||
      ev.category.toLowerCase().includes(q) ||
      ev.location.toLowerCase().includes(q)
    ).filter(ev =>
      loc === "" || ev.location.toLowerCase().includes(loc)
    );

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


function loadEventDetail() {
  if (!window.location.pathname.includes("event.html")) return;

  const params = new URLSearchParams(window.location.search);
  const id = parseInt(params.get("id"));
  const ev = events.find(e => e.id === id);
  if (!ev) return;

  // Store event for tickets page
  localStorage.setItem("selected_event", JSON.stringify(ev));

  // HERO SECTION
  document.getElementById("event-title").textContent = ev.title;
  document.getElementById("badge-category").textContent = ev.category;
  document.getElementById("badge-age").textContent = ev.ageRestriction;
  document.getElementById("badge-dress").textContent = ev.dressCode;

  document.getElementById("event-meta").textContent =
    `${ev.dateLabel} · ${ev.time} · ${ev.location}`;

  document.getElementById("event-submeta").textContent =
    `${ev.venueCapacity} capacity`;

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
  document.getElementById("get-tickets-btn-main").textContent = "Get Tickets";

  // STICKY CTA
  document.getElementById("sticky-cta-title").textContent = ev.title;
  document.getElementById("sticky-cta-price").textContent = ev.priceLabel;

  // ⭐ Load venue map
  if (ev.venue && ev.venue.lat && ev.venue.lng) {
    loadVenueMap(ev.venue.lat, ev.venue.lng);
  }

  // ⭐ Dynamic background image
  document.body.style.background = `url('${ev.image}') no-repeat center center fixed`;
  document.body.style.backgroundSize = "cover";
}


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
// REGISTER FORM (DEMO MODE)
// ===============================
const registerForm = document.getElementById("register-form");
if (registerForm) {
  registerForm.addEventListener("submit", e => {
    e.preventDefault();
    alert("Account created (demo mode)");
    window.location.href = "signin.html";
  });
}


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

