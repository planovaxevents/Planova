// ===============================
// STOCK EVENT DATA (UPGRADED)
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

  {
    id: 2,
    title: "Cell - Fiesta Fuego",
    category: "Live Music",
    date: "2026-06-10",
    dateLabel: "Sat 10 Jun",
    dateISO: "2026-06-10T18:00:00",
    time: "18:00–23:00",
    location: "Nottingham",
    price: 15,
    priceLabel: "From £15.00",
    image: "https://images.pexels.com/photos/167404/pexels-photo-167404.jpeg",
    description: "Live bands, cocktails and sunset views over the city.",

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
    ]
  },

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
  },

  {
    id: 7,
    title: "Birmingham Summer Carnival",
    category: "Festival",
    date: "2026-08-03",
    dateLabel: "Sun 3 Aug",
    dateISO: "2026-08-03T11:00:00",
    time: "11:00–22:00",
    location: "Birmingham",
    price: 28,
    priceLabel: "From £28.00",
    image: "https://images.pexels.com/photos/1763072/pexels-photo-1763072.jpeg",
    description: "A colourful outdoor carnival with food, music, dancers and live performers.",

    venueCapacity: 7000,
    ageRestriction: "All ages (Under 16 with adult)",
    dressCode: "Festival wear",
    genres: ["Carnival", "Dance", "Live Performers"],

    ticketAvailability: {
      standard: 1500,
      vip: 400,
      vvip: 80
    },

    addons: {
      queue_jump: true,
      drinks_tokens: true,
      afterparty: true,
      merch: true
    },

    promoCodes: {
      "CARNIVAL10": 0.10
    },

    reviews: [
      { stars: 5, text: "Amazing family-friendly festival!", when: "3 weeks ago" }
    ]
  },

  {
    id: 8,
    title: "Liverpool DnB Warehouse Rave",
    category: "Clubbing",
    date: "2026-05-30",
    dateLabel: "Fri 30 May",
    dateISO: "2026-05-30T23:00:00",
    time: "23:00–06:00",
    location: "Liverpool",
    price: 20,
    priceLabel: "From £20.00",
    image: "https://images.pexels.com/photos/1190296/pexels-photo-1190296.jpeg",
    description: "A heavy‑hitting DnB rave inside Liverpool’s iconic warehouse venue.",

    venueCapacity: 1200,
    ageRestriction: "18+",
    dressCode: "Casual / Ravewear",
    genres: ["DnB", "Jungle", "Bass"],

    ticketAvailability: {
      standard: 200,
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
      "DNB10": 0.10
    },

    reviews: [
      { stars: 5, text: "Warehouse vibes were insane!", when: "Last week" }
    ]
  },

  {
    id: 9,
    title: "Leeds Sunset Terrace Party",
    category: "Clubbing",
    date: "2026-06-22",
    dateLabel: "Sat 22 Jun",
    dateISO: "2026-06-22T17:00:00",
    time: "17:00–23:00",
    location: "Leeds",
    price: 14,
    priceLabel: "From £14.00",
    image: "https://images.pexels.com/photos/210922/pexels-photo-210922.jpeg",
    description: "A chilled terrace party with house, disco and summer cocktails.",

    venueCapacity: 300,
    ageRestriction: "18+",
    dressCode: "Summer casual",
    genres: ["House", "Disco", "Chill"],

    ticketAvailability: {
      standard: 80,
      vip: 10,
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
      { stars: 4, text: "Perfect summer vibes!", when: "2 weeks ago" }
    ]
  },

  {
    id: 10,
    title: "Sheffield Rock Night – Steel City Live",
    category: "Live Music",
    date: "2026-05-11",
    dateLabel: "Sun 11 May",
    dateISO: "2026-05-11T18:00:00",
    time: "18:00–23:00",
    location: "Sheffield",
    price: 16,
    priceLabel: "From £16.00",
    image: "https://images.pexels.com/photos/167636/pexels-photo-167636.jpeg",
    description: "A night of rock, metal and alternative bands from across the UK.",

    venueCapacity: 600,
    ageRestriction: "18+",
    dressCode: "Casual / Band tees",
    genres: ["Rock", "Metal", "Alternative"],

    ticketAvailability: {
      standard: 150,
      vip: 20,
      vvip: 0
    },

    addons: {
      queue_jump: false,
      drinks_tokens: true,
      afterparty: false,
      merch: true
    },

    promoCodes: {},

    reviews: [
      { stars: 5, text: "Rock fans will love this!", when: "1 month ago" }
    ]
  },

  {
    id: 11,
    title: "Bristol Drum & Bass Carnival",
    category: "Festival",
    date: "2026-07-05",
    dateLabel: "Sat 5 Jul",
    dateISO: "2026-07-05T13:00:00",
    time: "13:00–23:00",
    location: "Bristol",
    price: 32,
    priceLabel: "From £32.00",
    image: "https://images.pexels.com/photos/1190295/pexels-photo-1190295.jpeg",
    description: "Bristol’s legendary DnB carnival returns with huge headliners and street food.",

    venueCapacity: 8000,
    ageRestriction: "16+",
    dressCode: "Festival wear",
    genres: ["DnB", "Bass", "Electronic"],

    ticketAvailability: {
      standard: 2000,
      vip: 500,
      vvip: 100
    },

    addons: {
      queue_jump: true,
      drinks_tokens: true,
      afterparty: true,
      merch: true
    },

    promoCodes: {
      "BRISTOL15": 0.15
    },

    reviews: [
      { stars: 5, text: "The biggest DnB event of the year!", when: "3 weeks ago" }
    ]
  },

  {
    id: 12,
    title: "Cardiff Student Neon Rave",
    category: "Student Night",
    date: "2026-04-26",
    dateLabel: "Sat 26 Apr",
    dateISO: "2026-04-26T22:00:00",
    time: "22:00–03:00",
    location: "Cardiff",
    price: 6,
    priceLabel: "From £6.00",
    image: "https://images.pexels.com/photos/2747440/pexels-photo-2747440.jpeg",
    description: "A neon‑themed rave with glow sticks, UV paint and student drink deals.",

    venueCapacity: 900,
    ageRestriction: "18+ (Student ID required)",
    dressCode: "Neon / UV",
    genres: ["RnB", "Chart", "Dance"],

    ticketAvailability: {
      standard: 250,
      vip: 30,
      vvip: 0
    },

    addons: {
      queue_jump: true,
      drinks_tokens: false,
      afterparty: false,
      merch: false
    },

    promoCodes: {
      "NEON5": 0.05
    },

    reviews: [
      { stars: 5, text: "UV paint everywhere — loved it!", when: "Last week" }
    ]
  },
{
    id: 14,
    title: "Newcastle Summer Beats Festival",
    category: "Festival",
    date: "2026-08-18",
    dateLabel: "Sun 18 Aug",
    dateISO: "2026-08-18T12:00:00",
    time: "12:00–22:00",
    location: "Newcastle",
    price: 30,
    priceLabel: "From £30.00",
    image: "https://images.pexels.com/photos/1763073/pexels-photo-1763073.jpeg",
    description: "A summer festival with pop, dance and electronic artists across two stages.",

    venueCapacity: 9000,
    ageRestriction: "All ages (Under 16 with adult)",
    dressCode: "Festival wear",
    genres: ["Pop", "Dance", "Electronic"],

    ticketAvailability: {
      standard: 2500,
      vip: 600,
      vvip: 120
    },

    addons: {
      queue_jump: true,
      drinks_tokens: true,
      afterparty: true,
      merch: true
    },

    promoCodes: {
      "SUMMERBEATS10": 0.10,
      "VIP25": 0.25
    },

    reviews: [
      { stars: 5, text: "Huge stages and amazing energy!", when: "Last month" },
      { stars: 4, text: "VIP was definitely worth it.", when: "2 weeks ago" }
    ]
  }

];



















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


// ===============================
// EVENT DETAIL PAGE
// ===============================
function loadEventDetail() {
  if (!window.location.pathname.includes("event.html")) return;

  const params = new URLSearchParams(window.location.search);
  const id = parseInt(params.get("id"));
  const ev = events.find(e => e.id === id);
  if (!ev) return;

  // Store event for tickets page
  localStorage.setItem("selected_event", JSON.stringify(ev));

  document.getElementById("event-title").textContent = ev.title;
  document.getElementById("event-category").textContent = ev.category;
  document.getElementById("event-meta").textContent = `${ev.dateLabel} · ${ev.time} · ${ev.location}`;
  document.getElementById("event-description").textContent = ev.description;
  document.getElementById("event-price").textContent = ev.priceLabel;
  document.getElementById("event-image").src = ev.image;

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

