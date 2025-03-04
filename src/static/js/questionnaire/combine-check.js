document.addEventListener("DOMContentLoaded", () => {
    const checkBox = document.getElementById('dynamic-block')
    const btnAddMore = document.getElementById('add-one-more-block')
    const blockMuted = document.querySelector('.block-muted')

    btnAddMore.style.display = 'none'

    if  (checkBox.checked) {
        blockMuted.classList.remove('block-muted')
        btnAddMore.style.display = 'flex'
    }


    function toggleBlock() {
        if (checkBox.checked) {
            blockMuted.classList.remove('block-muted')
            btnAddMore.style.display = 'flex'
        }
        else {
            blockMuted.classList.add('block-muted')
            btnAddMore.style.display = 'none'
        }
    
    }

    checkBox.addEventListener('change', toggleBlock)
})