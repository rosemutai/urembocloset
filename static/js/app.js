const productGridLayout = document.getElementById('product-grid-layout')
const productListLayout = document.getElementById('product-list-layout')
const gridLayoutBtn = document.getElementById('grid-layout-btn')
const listLayoutBtn = document.getElementById('list-layout-btn')
const modal = document.getElementById('deleteModal');
const form = document.getElementById('deleteForm');
const text = document.getElementById('modalText');
const deleteProductBtn = document.getElementById('delete-btn')
const toast = document.getElementById('toast-success');


if (listLayoutBtn) {
    listLayoutBtn.addEventListener('click', () => {
        gridLayoutBtn.classList.remove('active')
        listLayoutBtn.classList.add('active')
        productGridLayout.classList.add('hidden')
        productListLayout.classList.remove('hidden')
        productListLayout.classList.add('grid')


    })
}

if (gridLayoutBtn) {
    gridLayoutBtn.addEventListener('click', () => {
        listLayoutBtn.classList.remove('active')
        productListLayout.classList.add('hidden')
        productGridLayout.classList.remove('hidden')
        productGridLayout.classList.add('grid')
        gridLayoutBtn.classList.add('active')
    })
}



function closeModal() {
  modal.classList.add('hidden');
}

if (deleteProductBtn){
    deleteProductBtn.addEventListener('click', () => {
        const product_id = deleteProductBtn.dataset.id;
        const itemName = deleteProductBtn.dataset.name;
        text.textContent = `Are you sure you want to delete? ${itemName}`;
        form.action = `/store/delete-product/${product_id}/`;  // Match your Django URL
        modal.classList.remove('hidden');
    })

}

const urlParams = new URLSearchParams(window.location.search);
const deletedProduct = urlParams.get('deleted');
if (deletedProduct) {
  document.getElementById('toast-message').textContent = `Product ${deletedProduct} deleted successfully.`;
  toast.classList.remove('hidden');
  toast.classList.add('flex');
  setTimeout(() => toast.classList.add('hidden'), 3000);
  history.replaceState(null, "", window.location.pathname);
//   flex
}


