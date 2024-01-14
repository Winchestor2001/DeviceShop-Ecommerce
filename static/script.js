let banner_image = document.querySelector('.banner__image')
let banner_header = document.querySelector('.banner__right__header')
let banner_a = document.querySelector('#view_products')
function banner_btn(btn, src) {
    let active = document.querySelector('.banner__left__btn-active')
    active.classList.remove('banner__left__btn-active')
    active.classList.add('banner__left__btn')
    btn.classList.remove('banner__left__btn')
    btn.classList.add('banner__left__btn-active')
    banner_image.style.backgroundImage = 'url(media/' + btn.id + ')';
    banner_header.textContent = btn.textContent
    banner_a.href = `/shop/${src}`
}