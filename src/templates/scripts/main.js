// SOSParser Report - Interactive JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Tab switching
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Remove active class from all tabs and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            this.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
            
            // Save current tab to sessionStorage
            sessionStorage.setItem('activeTab', targetTab);
        });
    });
    
    // Restore last active tab from sessionStorage
    const lastActiveTab = sessionStorage.getItem('activeTab');
    if (lastActiveTab) {
        const targetButton = document.querySelector(`[data-tab="${lastActiveTab}"]`);
        const targetContent = document.getElementById(lastActiveTab);
        
        if (targetButton && targetContent) {
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            targetButton.classList.add('active');
            targetContent.classList.add('active');
        }
    }
    
    // Subtab switching
    const subtabButtons = document.querySelectorAll('.subtab-button');
    
    subtabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetSubtab = this.getAttribute('data-subtab');
            
            // Get parent tab content to scope subtab changes
            const parentTab = this.closest('.tab-content');
            if (!parentTab) return;
            
            // Remove active class from all subtab buttons and contents in this tab
            const siblingButtons = parentTab.querySelectorAll('.subtab-button');
            const siblingContents = parentTab.querySelectorAll('.subtab-content');
            
            siblingButtons.forEach(btn => btn.classList.remove('active'));
            siblingContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked subtab and corresponding content
            this.classList.add('active');
            const targetContent = parentTab.querySelector(`#${targetSubtab}`);
            if (targetContent) {
                targetContent.classList.add('active');
            }
            
            // Save current subtab for this tab
            const parentTabId = parentTab.getAttribute('id');
            sessionStorage.setItem(`activeSubtab-${parentTabId}`, targetSubtab);
        });
    });
    
    // Restore last active subtabs
    tabContents.forEach(tabContent => {
        const tabId = tabContent.getAttribute('id');
        const lastSubtab = sessionStorage.getItem(`activeSubtab-${tabId}`);
        
        if (lastSubtab) {
            const targetButton = tabContent.querySelector(`[data-subtab="${lastSubtab}"]`);
            const targetContent = tabContent.querySelector(`#${lastSubtab}`);
            
            if (targetButton && targetContent) {
                const buttons = tabContent.querySelectorAll('.subtab-button');
                const contents = tabContent.querySelectorAll('.subtab-content');
                
                buttons.forEach(btn => btn.classList.remove('active'));
                contents.forEach(content => content.classList.remove('active'));
                
                targetButton.classList.add('active');
                targetContent.classList.add('active');
            }
        }
    });
});

// Toggle scenario details
function toggleScenarioDetails(header) {
    const details = header.nextElementSibling;
    const button = header.querySelector('.toggle-details');
    
    if (details.classList.contains('active')) {
        details.classList.remove('active');
        button.textContent = 'Show Details';
    } else {
        details.classList.add('active');
        button.textContent = 'Hide Details';
    }
}

// Add smooth scrolling to all links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
