class RSVPReader {
    constructor() {
        this.words = [];
        this.paragraphs = [];
        this.sentences = [];
        this.currentIndex = 0;
        this.isPlaying = false;
        this.wpm = 300;
        this.timer = null;
        this.sentencePause = 500;
        this.currentWordIndex = 0;
        this.sentenceEndIndex = -1;
        
        this.initializeElements();
        this.attachEventListeners();
    }
    
    initializeElements() {
        this.uploadSection = document.getElementById('uploadSection');
        this.readerSection = document.getElementById('readerSection');
        this.loading = document.getElementById('loading');
        this.error = document.getElementById('error');
        
        this.pdfInput = document.getElementById('pdfInput');
        this.ocrToggle = document.getElementById('ocrToggle');
        this.playPauseBtn = document.getElementById('playPauseBtn');
        this.resetBtn = document.getElementById('resetBtn');
        this.slowDownBtn = document.getElementById('slowDownBtn');
        this.speedUpBtn = document.getElementById('speedUpBtn');
        this.speedDisplay = document.getElementById('speedDisplay');
        this.backBtn = document.getElementById('backBtn');
        this.reviewBtn = document.getElementById('reviewBtn');
        this.retryBtn = document.getElementById('retryBtn');
        
        this.rsvpDisplay = document.getElementById('rsvpDisplay');
        this.focalLetter = document.getElementById('focalLetter');  // Fixed: renamed from pivotalLetter
        this.leftPart = document.getElementById('leftPart');
        this.rightPart = document.getElementById('rightPart');
        this.wordProgress = document.getElementById('wordProgress');
        this.progressBar = document.getElementById('progressBar');
        
        this.reviewPanel = document.getElementById('reviewPanel');
        this.closeReviewBtn = document.getElementById('closeReview');
        this.currentParagraph = document.getElementById('currentParagraph');
        this.currentSentence = document.getElementById('currentSentence');
        this.prevReviewBtn = document.getElementById('prevReviewBtn');
        this.nextReviewBtn = document.getElementById('nextReviewBtn');
        this.tabs = document.querySelectorAll('.tab');
        this.reviewItems = document.querySelectorAll('.review-item');
    }
    
    attachEventListeners() {
        this.pdfInput.addEventListener('change', (e) => this.handleFileUpload(e));
        this.playPauseBtn.addEventListener('click', () => this.togglePlayPause());
        this.resetBtn.addEventListener('click', () => this.reset());
        this.slowDownBtn.addEventListener('click', () => this.adjustSpeed(-50));
        this.speedUpBtn.addEventListener('click', () => this.adjustSpeed(50));
        this.backBtn.addEventListener('click', () => this.goBack());
        this.reviewBtn.addEventListener('click', () => this.openReview());
        this.retryBtn.addEventListener('click', () => this.hideError());
        
        this.closeReviewBtn.addEventListener('click', () => this.closeReview());
        this.prevReviewBtn.addEventListener('click', () => this.navigateReview(-1));
        this.nextReviewBtn.addEventListener('click', () => this.navigateReview(1));
        
        this.tabs.forEach(tab => {
            tab.addEventListener('click', () => this.switchTab(tab.dataset.tab));
        });
        
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
    }
    
    handleKeyboard(e) {
        if (e.code === 'Space') {
            e.preventDefault();
            this.togglePlayPause();
        } else if (e.code === 'ArrowLeft') {
            this.navigateReview(-1);
        } else if (e.code === 'ArrowRight') {
            this.navigateReview(1);
        } else if (e.code === 'ArrowUp') {
            this.adjustSpeed(50);
        } else if (e.code === 'ArrowDown') {
            this.adjustSpeed(-50);
        }
    }
    
    async handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        this.showLoading();
        
        const formData = new FormData();
        formData.append('file', file);
        formData.append('use_ocr', this.ocrToggle.checked);
        
        try {
            const response = await fetch('/upload-pdf', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) throw new Error('Failed to process PDF');
            
            const data = await response.json();
            this.loadData(data);
            this.showReader();
        } catch (error) {
            this.showError(error.message);
        }
    }
    
    loadData(data) {
        this.words = data.words;
        this.paragraphs = data.paragraphs;
        this.sentences = data.sentences;
        this.currentIndex = 0;
        this.currentWordIndex = 0;
        this.sentenceEndIndex = -1;
        this.updateProgress();
    }
    
    togglePlayPause() {
        if (this.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    }
    
    play() {
        if (this.currentIndex >= this.words.length) {
            this.currentIndex = 0;
        }
        
        this.isPlaying = true;
        this.playPauseBtn.textContent = '⏸ Pause';
        this.displayNextWord();
    }
    
    pause() {
        this.isPlaying = false;
        this.playPauseBtn.textContent = '▶ Play';
        if (this.timer) {
            clearTimeout(this.timer);
        }
    }
    
    displayNextWord() {
        if (this.currentIndex >= this.words.length) {
            this.pause();
            return;
        }
        
        const wordData = this.words[this.currentIndex];
        this.displayWord(wordData);
        
        this.currentWordIndex = this.currentIndex;
        
        let delay = 60000 / this.wpm;
        
        if (wordData.is_sentence_end) {
            this.sentenceEndIndex = this.currentIndex;
            delay += this.sentencePause;
        }
        
        this.updateProgress();
        
        if (this.isPlaying) {
            this.timer = setTimeout(() => {
                this.currentIndex++;
                this.displayNextWord();
            }, delay);
        }
    }
    
    displayWord(wordData) {
        const word = wordData.word;
        const focalLetters = wordData.focal_letters;
        
        // Get the primary focal letter index
        let focalIndex = Math.floor(word.length / 2);
        
        if (focalLetters.length > 0) {
            // Use the first (primary) focal letter from our improved model
            focalIndex = focalLetters[0].index;
        }
        
        // FIXED: Split word into left, focal, and right parts
        const leftText = word.substring(0, focalIndex);
        const focalChar = word[focalIndex] || '';
        const rightText = word.substring(focalIndex + 1);
        
        // Update the display (HTML order is already correct: left, focal, right)
        this.leftPart.textContent = leftText;
        this.focalLetter.textContent = focalChar;
        this.rightPart.textContent = rightText;
        
        // Update word progress
        this.wordProgress.textContent = `${this.currentIndex + 1} / ${this.words.length}`;
    }
    
    adjustSpeed(delta) {
        this.wpm = Math.max(100, Math.min(1000, this.wpm + delta));
        this.speedDisplay.textContent = `${this.wpm} WPM`;
    }
    
    reset() {
        this.pause();
        this.currentIndex = 0;
        this.currentWordIndex = 0;
        this.sentenceEndIndex = -1;
        this.updateProgress();
        this.displayWord({ word: '', focal_letters: [], is_sentence_end: false });
        this.wordProgress.textContent = `0 / ${this.words.length}`;
    }
    
    goBack() {
        this.pause();
        this.uploadSection.style.display = 'flex';
        this.readerSection.style.display = 'none';
        this.pdfInput.value = '';
    }
    
    updateProgress() {
        const progress = (this.currentIndex / this.words.length) * 100;
        this.progressBar.style.width = `${progress}%`;
    }
    
    openReview() {
        this.pause();
        this.reviewPanel.style.display = 'block';
        this.updateReviewContent();
    }
    
    closeReview() {
        this.reviewPanel.style.display = 'none';
    }
    
    updateReviewContent() {
        const wordData = this.words[this.currentWordIndex];
        const currentWord = wordData.word;
        
        let paragraphIndex = this.findParagraphIndex(currentWord);
        let sentenceIndex = this.findSentenceIndex(currentWord);
        
        this.currentParagraph.textContent = this.paragraphs[paragraphIndex] || 'No paragraph found';
        this.currentSentence.textContent = this.sentences[sentenceIndex] || 'No sentence found';
    }
    
    findParagraphIndex(word) {
        for (let i = 0; i < this.paragraphs.length; i++) {
            if (this.paragraphs[i].toLowerCase().includes(word.toLowerCase())) {
                return i;
            }
        }
        return 0;
    }
    
    findSentenceIndex(word) {
        for (let i = 0; i < this.sentences.length; i++) {
            if (this.sentences[i].toLowerCase().includes(word.toLowerCase())) {
                return i;
            }
        }
        return 0;
    }
    
    navigateReview(direction) {
        if (this.reviewItems[0].classList.contains('active')) {
            let paragraphIndex = this.findParagraphIndex(this.words[this.currentWordIndex].word);
            paragraphIndex = Math.max(0, Math.min(this.paragraphs.length - 1, paragraphIndex + direction));
            this.currentParagraph.textContent = this.paragraphs[paragraphIndex];
        } else {
            let sentenceIndex = this.findSentenceIndex(this.words[this.currentWordIndex].word);
            sentenceIndex = Math.max(0, Math.min(this.sentences.length - 1, sentenceIndex + direction));
            this.currentSentence.textContent = this.sentences[sentenceIndex];
        }
    }
    
    switchTab(tabName) {
        this.tabs.forEach(tab => tab.classList.remove('active'));
        this.reviewItems.forEach(item => item.classList.remove('active'));
        
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        document.getElementById(`current${tabName.charAt(0).toUpperCase() + tabName.slice(1)}`).classList.add('active');
    }
    
    showLoading() {
        this.uploadSection.style.display = 'none';
        this.readerSection.style.display = 'none';
        this.loading.style.display = 'flex';
        this.error.style.display = 'none';
    }
    
    showReader() {
        this.loading.style.display = 'none';
        this.readerSection.style.display = 'flex';
        this.error.style.display = 'none';
    }
    
    showError(message) {
        this.loading.style.display = 'none';
        this.readerSection.style.display = 'none';
        this.error.style.display = 'flex';
        document.getElementById('errorMessage').textContent = message;
    }
    
    hideError() {
        this.error.style.display = 'none';
        this.uploadSection.style.display = 'flex';
    }
}

// Initialize the reader when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new RSVPReader();
});