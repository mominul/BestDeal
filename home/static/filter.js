
$(document).ready(function() {
    $('#filter-button').click(function() {
        // Get the user-entered maximum price
        const maxPriceText = $('#max_price').val(); // Example input: "৳ 95,000"
        
        // Extract the numerical part and convert it to a number
        const maxPrice = parseFloat(maxPriceText.replace(/[^0-9.]/g, '')); // Converts "৳ 95,000" to 95000

        // Loop through product items and hide/show based on price
        $('.item').each(function() {
            const itemPriceText = $(this).data('price'); // Example: "৳ 103,999"
            
            // Extract the numerical part and convert it to a number
            const itemPrice = parseFloat(itemPriceText.replace(/[^0-9.]/g, ''));

            if (!isNaN(itemPrice) && itemPrice <= maxPrice) {
                $(this).show(); // Show the product
            } else {
                $(this).hide(); // Hide the product
            }
        });
    });
});
