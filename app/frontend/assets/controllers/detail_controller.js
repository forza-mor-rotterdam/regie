import { Controller } from '@hotwired/stimulus';

export default class extends Controller {

    static targets = ['selectedImage', 'thumbList', 'imageSliderContainer']

    initialize() {
        if(this.hasThumbListTarget) {
            this.thumbListTarget.getElementsByTagName('li')[0].classList.add('selected')
        }
    }

    openModal() {
        console.log("openModal")
        const modal = document.querySelector('.modal');
        const modalBackdrop = document.querySelector('.modal-backdrop');

        console.log('modal', modal)
        console.log('modalBackDrop', modalBackdrop)
        modal.classList.add('show');
        modalBackdrop.classList.add('show');
        document.body.classList.add('show-modal');
    }

    closeModal() {
        console.log('closeModal')
        const modal = document.querySelector('.modal');
        const modalBackdrop = document.querySelector('.modal-backdrop');
        modal.classList.remove('show');
        modalBackdrop.classList.remove('show');
        document.body.classList.remove('show-modal');
    }

    onScrollSlider(e) {
        this.highlightThumb(Math.floor(this.imageSliderContainerTarget.scrollLeft / this.imageSliderContainerTarget.offsetWidth))
    }

    selectImage(e) {
        console.log("selectImage", e.params.imageIndex)
        this.imageSliderContainerTarget.scrollTo({left: (Number(e.params.imageIndex) - 1) * this.imageSliderContainerTarget.offsetWidth, top: 0})
        this.deselectThumbs(e.target.closest('ul'));
        e.target.closest('li').classList.add('selected');
    }

    highlightThumb(index) {
        this.deselectThumbs(this.thumbListTarget)
        this.thumbListTarget.getElementsByTagName('li')[index].classList.add('selected')
    }

    deselectThumbs(list) {
        for (const item of list.querySelectorAll('li')) {
            item.classList.remove('selected');
        }
    }

    cancelInformatieToevoegen(e) {
        console.log("cancelInformatieToevoegen")
        const form = e.target.closest("form")
        // form.find(input["type=file"]).value=null
        form.reset();
        e.target.closest('details').open = false;
    }

}
