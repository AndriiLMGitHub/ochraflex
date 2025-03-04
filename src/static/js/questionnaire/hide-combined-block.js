document.addEventListener('DOMContentLoaded', () => {
    const combinedBlock = document.getElementById("combined-block");
    if (combinedBlock.children.length === 0) {
      combinedBlock.style.display = 'none';
    }
    else {
      combinedBlock.style.display = 'block';
    }
  })