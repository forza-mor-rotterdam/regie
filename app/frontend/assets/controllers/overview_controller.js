import { Controller } from '@hotwired/stimulus';

export default class extends Controller {

    connect() {

    }

    openModal(e) {
        const modal = this.element.querySelector('.modal');
        const modalBackdrop = this.element.querySelector('.modal-backdrop');

        modal.classList.add('show');
        modalBackdrop.classList.add('show');
        document.body.classList.add('show-modal');
    }

    closeModal() {
        const modal = this.element.querySelector('.modal');
        const modalBackdrop = this.element.querySelector('.modal-backdrop');
        modal.classList.remove('show');
        modalBackdrop.classList.remove('show');
        document.body.classList.remove('show-modal');
    }

    setUrl(e) {
        const nextURL = `${window.location.href.split('?')[0]}${e.target.href.substring(e.target.href.indexOf("?"))}`;
        const nextTitle = document.title;
        const nextState = { additionalInformation: 'Updated the URL with JS' };

        // This will create a new entry in the browser's history, without reloading
        window.history.pushState(nextState, nextTitle, nextURL);
    }
}
