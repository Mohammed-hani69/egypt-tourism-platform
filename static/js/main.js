// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Rating system for review form
    const ratingStars = document.querySelectorAll('.rating-select .star');
    const ratingInput = document.getElementById('rating');

    if (ratingStars.length > 0 && ratingInput) {
        ratingStars.forEach(star => {
            star.addEventListener('click', function() {
                const value = this.getAttribute('data-value');
                ratingInput.value = value;
                
                // Update visual selection
                ratingStars.forEach(s => {
                    if (s.getAttribute('data-value') <= value) {
                        s.classList.add('selected');
                    } else {
                        s.classList.remove('selected');
                    }
                });
            });
        });
    }

    // Handle region filter in attractions page
    const regionFilter = document.getElementById('region-filter');
    if (regionFilter) {
        regionFilter.addEventListener('change', function() {
            const regionId = this.value;
            if (regionId) {
                window.location.href = `/attractions?region=${regionId}`;
            } else {
                window.location.href = '/attractions';
            }
        });
    }

    // Handle sort filter in attractions page
    const sortFilter = document.getElementById('sort-filter');
    if (sortFilter) {
        sortFilter.addEventListener('change', function() {
            const sortBy = this.value;
            const urlParams = new URLSearchParams(window.location.search);
            urlParams.set('sort', sortBy);
            window.location.href = `/attractions?${urlParams.toString()}`;
        });
    }

    // Search form validation
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const searchInput = this.querySelector('input[name="q"]');
            if (!searchInput.value.trim()) {
                e.preventDefault();
                alert('Please enter a search term');
            }
        });
    }

    // Language selector
    const languageLinks = document.querySelectorAll('.language-selector a');
    languageLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const language = this.getAttribute('data-language');
            
            // Create and append a form to change the language
            const form = document.createElement('form');
            form.method = 'GET';
            form.action = `/set_language/${language}`;
            document.body.appendChild(form);
            form.submit();
        });
    });

    // Display stars based on rating
    function displayRatingStars() {
        const ratingElements = document.querySelectorAll('.rating-display');
        
        ratingElements.forEach(element => {
            const rating = parseFloat(element.getAttribute('data-rating'));
            const starsTotal = 5;
            const starsPercentage = (rating / starsTotal) * 100;
            
            // Update stars width
            const starsFilled = element.querySelector('.rating-stars');
            if (starsFilled) {
                starsFilled.style.width = `${starsPercentage}%`;
            }
        });
    }

    // Call function to display rating stars
    displayRatingStars();
});

// Render average rating for attractions
function renderRating(rating) {
    if (!rating) return "No ratings yet";
    
    const fullStar = '<i class="fas fa-star text-warning"></i>';
    const halfStar = '<i class="fas fa-star-half-alt text-warning"></i>';
    const emptyStar = '<i class="far fa-star text-warning"></i>';
    
    let stars = '';
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    
    for (let i = 1; i <= 5; i++) {
        if (i <= fullStars) {
            stars += fullStar;
        } else if (i === fullStars + 1 && hasHalfStar) {
            stars += halfStar;
        } else {
            stars += emptyStar;
        }
    }
    
    return `${stars} <span class="ms-1">(${rating.toFixed(1)})</span>`;
}
