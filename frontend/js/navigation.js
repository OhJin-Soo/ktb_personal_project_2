// Navigation utility for single-page app routing
const Navigation = {
    currentPage: null,

    // Initialize navigation
    init() {
        this.handleRoute();
        window.addEventListener('hashchange', () => this.handleRoute());
    },

    // Handle route changes
    handleRoute() {
        const hash = window.location.hash.slice(1) || 'login';
        this.navigateTo(hash);
    },

    // Navigate to a page
    navigateTo(page) {
        // Check authentication for protected pages
        const protectedPages = ['posts', 'post', 'makepost', 'editpost', 'editprofile', 'editpassword'];
        
        if (protectedPages.includes(page) && !Auth.isAuthenticated()) {
            this.navigateTo('login');
            return;
        }

        // Show the requested page
        this.showPage(page);
        this.currentPage = page;
    },

    // Show a specific page
    showPage(page) {
        // Hide all pages
        const pages = document.querySelectorAll('.page');
        pages.forEach(p => {
            p.style.display = 'none';
            p.classList.remove('active');
        });

        // Show requested page
        const targetPage = document.getElementById(`${page}-page`);
        if (targetPage) {
            targetPage.style.display = 'block';
            targetPage.classList.add('active');
            window.scrollTo(0, 0);
        } else {
            console.error(`Page ${page} not found`);
        }

        // Update navigation active state
        this.updateNavigation(page);
    },

    // Update navigation active state
    updateNavigation(activePage) {
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${activePage}`) {
                link.classList.add('active');
            }
        });
    },

    // Redirect to a page
    redirectTo(page) {
        window.location.hash = page;
    }
};

