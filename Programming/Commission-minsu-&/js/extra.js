function startLoading() {
    const pb = document.getElementById('progress-bar');
    const st = document.getElementById('loading-status-text');
    let width = 0;
    
    const interval = setInterval(() => {
        width += Math.random() * 15;
        if (width >= 100) {
            width = 100;
            clearInterval(interval);
            setTimeout(() => {
                document.getElementById('loading-screen').style.opacity = '0';
                setTimeout(() => {
                    document.getElementById('loading-screen').style.display = 'none';
                    document.getElementById('main-content').style.display = 'block';
                }, 500);
            }, 500);
        }
        pb.style.width = width + '%';
        st.innerText = width > 50 ? "Accessing Secure Data..." : "Restoring Fragments...";
    }, 150);
}

window.addEventListener('DOMContentLoaded', startLoading);