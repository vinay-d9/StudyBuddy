/**
 * Resume Upload Modal - Handles modal flow and skill extraction
 */

class ResumeModal {
    constructor() {
        this.modalOverlay = null;
        this.modal = null;
        this.showModalTimeout = null;
        this.init();
    }

    init() {
        console.log('🎯 ResumeModal.init() - Starting initialization...');
        
        // Wait for DOM to be fully ready
        if (document.readyState !== 'loading') {
            this.initializeElements();
        } else {
            document.addEventListener('DOMContentLoaded', () => this.initializeElements());
        }
    }

    initializeElements() {
        console.log('📱 DOM is ready, initializing elements...');
        
        this.modalOverlay = document.getElementById('resume-modal-overlay');
        this.modal = document.getElementById('resume-modal');
        
        if (!this.modalOverlay) {
            console.error('❌ CRITICAL: resume-modal-overlay not found');
            return;
        }
        if (!this.modal) {
            console.error('❌ CRITICAL: resume-modal element not found');
            return;
        }
        
        console.log('✅ Modal elements found:', {
            overlay: !!this.modalOverlay,
            modal: !!this.modal
        });
        
        this.setupEventListeners();
        this.checkSessionAndShow();
    }

    setupEventListeners() {
        console.log('🔗 Setting up event listeners...');
        
        // Close button
        const closeBtn = document.querySelector('.resume-modal-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                console.log('❌ Close button clicked');
                this.close();
            });
            console.log('   ✅ Close button listener attached');
        } else {
            console.warn('   ⚠️ Close button not found');
        }

        // Overlay click to close
        if (this.modalOverlay) {
            this.modalOverlay.addEventListener('click', (e) => {
                if (e.target === this.modalOverlay) {
                    console.log('❌ Overlay backdrop clicked');
                    this.close();
                }
            });
            console.log('   ✅ Overlay click listener attached');
        }

        // YES button - show upload form
        const yesBtn = document.getElementById('resume-modal-yes');
        if (yesBtn) {
            yesBtn.addEventListener('click', () => {
                console.log('✅ YES button clicked - showing upload form');
                this.showUploadForm();
            });
            console.log('   ✅ YES button listener attached');
        } else {
            console.warn('   ⚠️ YES button not found');
        }

        // NO button - close and show tip
        const noBtn = document.getElementById('resume-modal-no');
        if (noBtn) {
            noBtn.addEventListener('click', () => {
                console.log('❌ NO button clicked - skipping upload');
                this.close();
            });
            console.log('   ✅ NO button listener attached');
        } else {
            console.warn('   ⚠️ NO button not found');
        }

        // Upload form handlers
        const uploadBtn = document.getElementById('resume-upload-submit');
        if (uploadBtn) {
            uploadBtn.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('🚀 Upload button clicked');
                this.submitResume();
            });
            console.log('   ✅ Upload button listener attached');
        } else {
            console.warn('   ⚠️ Upload button not found');
        }

        const fileInput = document.getElementById('resume-file-input');
        if (fileInput) {
            fileInput.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    console.log(`📄 File selected: ${file.name} (${(file.size / 1024).toFixed(2)} KB)`);
                    const valid = this.validateFile(file);
                    const submitBtn = document.getElementById('resume-upload-submit');
                    if (submitBtn) {
                        submitBtn.disabled = !valid;
                        console.log(`   ${valid ? '✅' : '❌'} Submit button ${valid ? 'enabled' : 'disabled'}`);
                    }
                }
            });
            console.log('   ✅ File input change listener attached');
        } else {
            console.warn('   ⚠️ File input not found');
        }
    }

    checkSessionAndShow() {
        console.log('🔍 Checking for existing resume...');
        
        // Check if modal was already shown in this session
        if (sessionStorage.getItem('resume_modal_shown')) {
            console.log('ℹ️ Modal already shown in this session - skipping');
            return;
        }

        // Check if user has a resume already
        console.log('   Fetching /api/resume/latest...');
        fetch('/api/resume/latest')
            .then(r => {
                console.log(`   API Response status: ${r.status}`);
                return r.json();
            })
            .then(data => {
                console.log('   API Response data:', data);
                
                // Determine if should show modal
                const hasResume = data && data.resume && data.resume.id;
                console.log(`   User has existing resume: ${hasResume}`);
                
                if (hasResume) {
                    console.log('ℹ️ User has existing resume - modal will not show');
                    sessionStorage.setItem('resume_modal_shown', 'true');
                    return;
                }

                console.log('📝 No existing resume - will show modal after delay');
                sessionStorage.setItem('resume_modal_shown', 'true');
                
                // Show modal after slight delay for UX
                this.showModalTimeout = setTimeout(() => {
                    console.log('👁️ Showing resume modal...');
                    this.show();
                }, 800);
            })
            .catch((err) => {
                // If API fails, still show modal
                console.warn('⚠️ Resume API check error:', err.message);
                sessionStorage.setItem('resume_modal_shown', 'true');
                
                this.showModalTimeout = setTimeout(() => {
                    console.log('👁️ Showing resume modal (API error fallback)...');
                    this.show();
                }, 800);
            });
    }

    show() {
        if (!this.modalOverlay || !this.modal) {
            console.error('❌ Cannot show modal - elements missing');
            return;
        }
        
        console.log('✨ Making modal visible...');
        this.modalOverlay.classList.add('active');
        console.log('   ✅ Modal is now visible');
    }

    close() {
        if (!this.modalOverlay) {
            console.warn('⚠️ Cannot close - overlay missing');
            return;
        }
        
        if (this.showModalTimeout) {
            clearTimeout(this.showModalTimeout);
        }
        
        console.log('🚪 Hiding modal...');
        this.modalOverlay.classList.remove('active');
        console.log('   ✅ Modal is now hidden');
    }

    showUploadForm() {
        const form = document.getElementById('resume-upload-form');
        const buttons = document.getElementById('resume-modal-buttons');
        
        if (!form) {
            console.error('❌ Upload form not found');
            return;
        }
        
        console.log('📋 Showing upload form...');
        form.classList.add('active');
        if (buttons) buttons.style.display = 'none';
        
        // Focus on file input
        setTimeout(() => {
            const fileInput = document.getElementById('resume-file-input');
            if (fileInput) {
                fileInput.focus();
                console.log('   ✅ File input focused');
            }
        }, 100);
    }

    resetForm() {
        console.log('🔄 Resetting upload form...');
        
        const form = document.getElementById('resume-upload-form');
        const buttons = document.getElementById('resume-modal-buttons');
        const status = document.getElementById('resume-upload-status');
        const fileInput = document.getElementById('resume-file-input');

        if (form) form.classList.remove('active');
        if (buttons) buttons.style.display = 'flex';
        if (status) {
            status.classList.remove('show', 'success', 'error', 'loading');
            status.innerHTML = '';
        }
        if (fileInput) fileInput.value = '';
        
        console.log('   ✅ Form reset complete');
    }

    validateFile(file) {
        const maxSize = 10 * 1024 * 1024; // 10MB
        const allowedExtensions = ['pdf', 'txt', 'doc', 'docx'];

        if (file.size > maxSize) {
            const msg = 'File too large (max 10MB)';
            console.warn(`❌ ${msg}`);
            this.showUploadStatus(msg, 'error');
            return false;
        }

        const ext = file.name.split('.').pop().toLowerCase();
        if (!allowedExtensions.includes(ext)) {
            const msg = `File type .${ext} not allowed (use PDF, DOC, DOCX, or TXT)`;
            console.warn(`❌ ${msg}`);
            this.showUploadStatus(msg, 'error');
            return false;
        }

        console.log('✅ File validation passed');
        return true;
    }

    showUploadStatus(message, type = 'info') {
        const status = document.getElementById('resume-upload-status');
        if (!status) {
            console.warn('⚠️ Status element not found, logging instead:', message);
            return;
        }
        
        status.innerHTML = message;
        status.className = `upload-status show ${type}`;
        
        console.log(`   [${type.toUpperCase()}] ${message}`);
        
        // Auto-hide success messages
        if (type === 'success') {
            setTimeout(() => {
                if (status) {
                    status.classList.remove('show');
                }
            }, 3000);
        }
    }

    async submitResume() {
        const fileInput = document.getElementById('resume-file-input');
        
        if (!fileInput || !fileInput.files[0]) {
            this.showUploadStatus('Please select a file', 'error');
            return;
        }

        const file = fileInput.files[0];
        console.log(`\n📤 RESUME UPLOAD STARTED`);
        console.log(`   File: ${file.name} (${(file.size / 1024).toFixed(2)} KB)`);
        
        if (!this.validateFile(file)) {
            return;
        }

        this.showUploadStatus('Uploading and extracting skills...', 'loading');
        console.log('   Status: Uploading...');

        try {
            // Step 1: Upload resume
            console.log('\n📤 STEP 1: Uploading file...');
            const formData = new FormData();
            formData.append('file', file);

            const uploadResponse = await fetch('/api/resume/upload', {
                method: 'POST',
                body: formData
            });

            console.log(`   Response status: ${uploadResponse.status}`);
            
            if (!uploadResponse.ok) {
                const errorData = await uploadResponse.json();
                throw new Error(`Upload failed: ${errorData.error || 'Unknown error'}`);
            }

            const uploadData = await uploadResponse.json();
            console.log('   Upload response:', uploadData);

            if (!uploadData.id) {
                throw new Error('No resume ID returned from server');
            }

            const resumeId = uploadData.id;
            console.log(`   ✅ Resume uploaded successfully with ID: ${resumeId}`);

            // Step 2: Extract skills
            console.log('\n🔍 STEP 2: Extracting skills...');
            this.showUploadStatus('Extracting skills from your resume...', 'loading');

            const skillsResponse = await fetch('/api/resume/extract-skills', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ resume_id: resumeId })
            });

            console.log(`   Response status: ${skillsResponse.status}`);
            
            if (!skillsResponse.ok) {
                const errorData = await skillsResponse.json();
                throw new Error(`Skill extraction failed: ${errorData.error || errorData.message || 'Unknown error'}`);
            }

            const skillsData = await skillsResponse.json();
            console.log('   Skills response:', skillsData);

            if (!skillsData.success) {
                throw new Error(skillsData.message || skillsData.error || 'Skill extraction failed');
            }

            console.log(`   ✅ Skills extracted: ${skillsData.skills_extracted} skills found`);
            console.log('   Skills:', skillsData.skills);

            // Success
            this.showUploadStatus(skillsData.message || 'Resume processed successfully!', 'success');
            console.log('\n✅ RESUME UPLOAD COMPLETE');

            // Close modal after success
            setTimeout(() => {
                console.log('🔄 Closing modal and reloading page...');
                this.close();
                this.resetForm();
                
                // Reload page to update UI
                setTimeout(() => {
                    console.log('🔄 Page reload triggered');
                    location.reload();
                }, 1000);
            }, 2000);

        } catch (err) {
            console.error('\n❌ RESUME UPLOAD FAILED');
            console.error('   Error:', err.message);
            console.error('   Stack:', err.stack);
            
            this.showUploadStatus(`Error: ${err.message}`, 'error');
        }
    }
}

// Initialize modal immediately
console.log('🚀 Resume Modal System Loading...');
const resumeModal = new ResumeModal();

