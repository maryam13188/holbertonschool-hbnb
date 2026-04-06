/* ============================================================
   scripts.js — HBnB Part 4
   Task 2: Login functionality
   ============================================================ */

const API_URL = 'http://127.0.0.1:5000/api/v1';

/* ============================================================
   UTILITY: Cookie helpers
   ============================================================ */
function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) return value;
    }
    return null;
}

function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value}; expires=${expires.toUTCString()}; path=/`;
}

/* ============================================================
   TASK 2: LOGIN
   ============================================================ */
async function loginUser(email, password) {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    return response;
}

/* ============================================================
   PAGE: LOGIN (login.html)
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {

    /* ---------- LOGIN FORM ---------- */
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email    = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
            const errorMsg = document.getElementById('error-message');

            try {
                const response = await loginUser(email, password);

                if (response.ok) {
                    const data = await response.json();
                    setCookie('token', data.access_token);
                    window.location.href = 'index.html';
                } else {
                    errorMsg.style.display = 'block';
                }
            } catch (error) {
                errorMsg.style.display = 'block';
                errorMsg.textContent   = 'Connection error. Please try again.';
            }
        });
    }

    /* ---------- INDEX PAGE: check auth + fetch places ---------- */
    const placesList = document.getElementById('places-list');
    if (placesList) {
        checkAuthIndex();
        setupPriceFilter();
    }

    /* ---------- PLACE DETAILS PAGE ---------- */
    const placeDetails = document.getElementById('place-details');
    if (placeDetails) {
        const placeId = getPlaceIdFromURL();
        const token   = getCookie('token');

        // Show/hide login link
        const loginLink = document.getElementById('login-link');
        if (loginLink) {
            loginLink.style.display = token ? 'none' : 'block';
        }

        // Show add-review section only if authenticated
        const addReviewSection = document.getElementById('add-review');
        if (addReviewSection) {
            addReviewSection.style.display = token ? 'block' : 'none';
        }

        if (placeId) {
            fetchPlaceDetails(token, placeId);
        }

        // Handle inline review form on place.html
        const reviewForm = document.getElementById('review-form');
        if (reviewForm && placeId) {
            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                const text   = document.getElementById('review-text').value.trim();
                const rating = parseInt(document.getElementById('rating').value);
                await submitReview(token, placeId, text, rating);
            });
        }
    }

    /* ---------- ADD REVIEW PAGE (add_review.html) ---------- */
    const reviewForm = document.getElementById('review-form');
    if (reviewForm && !document.getElementById('place-details')) {
        const token   = checkAuthAddReview();
        const placeId = getPlaceIdFromURL();

        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const text   = document.getElementById('review').value.trim();
            const rating = parseInt(document.getElementById('rating').value);
            await submitReview(token, placeId, text, rating);
        });
    }

});

/* ============================================================
   INDEX PAGE HELPERS
   ============================================================ */
let allPlaces = [];

function checkAuthIndex() {
    const token     = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'block';
    }

    fetchPlaces(token);
}

async function fetchPlaces(token) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(`${API_URL}/places/`, { headers });
        if (!response.ok) throw new Error('Failed to fetch places');

        const places = await response.json();
        allPlaces    = places;
        displayPlaces(places);
    } catch (error) {
        const list = document.getElementById('places-list');
        if (list) list.innerHTML = '<p style="color: var(--text-light);">Could not load places. Please try again later.</p>';
    }
}

function displayPlaces(places) {
    const list = document.getElementById('places-list');
    if (!list) return;
    list.innerHTML = '';

    if (places.length === 0) {
        list.innerHTML = '<p style="color: var(--text-light);">No places found.</p>';
        return;
    }

    places.forEach(place => {
        const card = document.createElement('div');
        card.className    = 'place-card';
        card.dataset.price = place.price;

        card.innerHTML = `
            <h3>${place.title}</h3>
            <p class="price">$${place.price} / night</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        list.appendChild(card);
    });
}

function setupPriceFilter() {
    const filter = document.getElementById('price-filter');
    if (!filter) return;

    filter.addEventListener('change', (event) => {
        const selected = event.target.value;
        const cards    = document.querySelectorAll('.place-card');

        cards.forEach(card => {
            const price = parseFloat(card.dataset.price);
            if (selected === 'all' || price <= parseFloat(selected)) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });
    });
}

/* ============================================================
   PLACE DETAILS HELPERS
   ============================================================ */
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(`${API_URL}/places/${placeId}`, { headers });
        if (!response.ok) throw new Error('Place not found');

        const place = await response.json();
        displayPlaceDetails(place);
        fetchReviews(token, placeId);
    } catch (error) {
        const section = document.getElementById('place-details');
        if (section) section.innerHTML = '<p>Could not load place details.</p>';
    }
}

function displayPlaceDetails(place) {
    const section = document.getElementById('place-details');
    if (!section) return;

    const amenitiesHTML = place.amenities && place.amenities.length > 0
        ? place.amenities.map(a => `<span class="amenity-tag">${a.name || a}</span>`).join('')
        : '<span class="amenity-tag">None listed</span>';

    section.innerHTML = `
        <div class="place-details">
            <h1>${place.title}</h1>
            <div class="place-info">
                <p><strong>Host:</strong> ${place.owner_id || 'N/A'}</p>
                <p><strong>Price:</strong> $${place.price} / night</p>
                <p><strong>Location:</strong> ${place.latitude}, ${place.longitude}</p>
                <p><strong>Description:</strong> ${place.description || 'No description provided.'}</p>
            </div>
            <div>
                <strong>Amenities:</strong>
                <div class="amenities-list">${amenitiesHTML}</div>
            </div>
        </div>
    `;
}

async function fetchReviews(token, placeId) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(`${API_URL}/places/${placeId}/reviews`, { headers });
        if (!response.ok) return;

        const reviews = await response.json();
        displayReviews(reviews);
    } catch (error) {
        console.error('Could not load reviews');
    }
}

function displayReviews(reviews) {
    const section = document.getElementById('reviews');
    if (!section) return;

    section.innerHTML = '<h2>Reviews</h2>';

    if (!reviews || reviews.length === 0) {
        section.innerHTML += '<p style="color: var(--text-light);">No reviews yet. Be the first!</p>';
        return;
    }

    reviews.forEach(review => {
        const stars = '⭐'.repeat(review.rating || 0);
        const card  = document.createElement('div');
        card.className = 'review-card';
        card.innerHTML = `
            <p class="reviewer">Anonymous</p>
            <p class="rating">${stars}</p>
            <p>${review.text}</p>
        `;
        section.appendChild(card);
    });
}

/* ============================================================
   ADD REVIEW HELPERS
   ============================================================ */
function checkAuthAddReview() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
    }
    return token;
}

async function submitReview(token, placeId, text, rating) {
    try {
        const response = await fetch(`${API_URL}/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type':  'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text:     text,
                rating:   rating,
                place_id: placeId
            })
        });

        handleReviewResponse(response);
    } catch (error) {
        alert('Connection error. Please try again.');
    }
}

async function handleReviewResponse(response) {
    if (response.ok) {
        alert('Review submitted successfully!');
        // Clear the form
        const form = document.getElementById('review-form');
        if (form) form.reset();
        // Redirect back to place page if on add_review.html
        const placeId = getPlaceIdFromURL();
        if (placeId && window.location.pathname.includes('add_review')) {
            window.location.href = `place.html?id=${placeId}`;
        }
    } else {
        const data = await response.json().catch(() => ({}));
        alert('Failed to submit review: ' + (data.error || response.statusText));
    }
}
