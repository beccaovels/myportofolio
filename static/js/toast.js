let toastTimer;

function showToast(title, message, type = 'normal', duration = 3000) {
    const toastComponent = document.getElementById('toast-component');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');

    if (!toastComponent) return;

    // remove previous type class
    toastComponent.classList.remove('toast-success', 'toast-error','toast-normal');

    // apply new class based on type
    if (type == 'success') {
        toastComponent.classList.add('toast-success');
    } else if (type == 'error') {
        toastComponent.classList.add('toast-error');
    } else {
        toastComponent.classList.add('toast-normal');
    }

    // update the text content
    toastTitle.textContent = title;
    toastMessage.textContent = message;

    // cancel the previous timer if a toast is still showing
    clearTimeout(toastTimer);

    // show animation
    if (!toastComponent.matches(':popover-open')) {
        toastComponent.showPopover();
        void toastComponent.offsetHeight; // force a style recalculation so transition runs
    }
    toastComponent.classList.remove('toast-hidden');
    toastComponent.classList.add('toast-show');

    // auto hide animation
    toastTimer = setTimeout(() => {
        toastComponent.classList.remove('toast-show');
        toastComponent.classList.add('toast-hidden');
        toastTimer = setTimeout(() => toastComponent.hidePopover(), 300);
    }, duration);
}