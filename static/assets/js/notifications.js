$(document).ready(function() {
    function displayNotifications() {
        $.ajax({
            url: '/display_notifications/',
            method: 'GET',
            success: function(response) {
                if (response.success) {
                    var notifications = response.result;
                    var notificationScroll = $('#notificationScroll');
                    var notificationCount = $('#notificationCount');
                    
                    notificationScroll.empty();
                    notificationCount.text(notifications.length); // Set notification count

                    notifications.forEach(function(notification) {
                        var notificationItem = `
                            <a class="dropdown-item preview-item" data-id="${notification.ID}">
                                <div class="preview-thumbnail">
                                    <div class="preview-icon bg-success">
                                        <i class="ti-info-alt"></i>
                                    </div>
                                </div>
                                <div class="preview-item-content">
                                    <h6 class="preview-subject font-weight-medium">${notification.Title}</h6>
                                    <p class="text-muted mb-0">${notification.Description}</p>
                                </div>
                            </a>
                        `;
                        notificationScroll.append(notificationItem);
                    });
                } else {
                    console.error('Failed to fetch notifications');
                }
            },
            error: function(xhr, status, error) {
                console.error('Error fetching notifications:', error);
            }
        });
    }

    // Function to handle click on notification items
    $(document).on('click', '.preview-item', function() {
        var notificationID = $(this).data('id');
        console.log('Clicked notification ID:', notificationID);

        // Perform any action with the notification ID here
    });

    // Call the function to display notifications when the document is ready
    displayNotifications();
});
