(function() {
    // Your code here
    function boot() {
        if (!window.frappe || !frappe.session || frappe.session.user === "Guest") {
            return;
        }
        frappe.router.on("change", () => {
            const route = frappe.get_route();
            if (route[0] !== "List" && route[1] !== "Item") return;
            const original_settings = frappe.listview_settings["Item"] || {};
            frappe.listview_settings['Item'] = {
                ...original_settings,
                onload: function(listview) {
                    move_column(listview, "name", 2);
                    listview.render();
                }
            };
        });
        function move_column(listview, fieldname, new_index) {
            const cols = listview.columns || [];

            const old_index = cols.findIndex(col => {
                return col?.df?.fieldname === fieldname || col?.type === fieldname;
            });

            if (old_index === -1) {
                console.warn("Column not found:", fieldname, cols);
                return;
            }

            const [col] = cols.splice(old_index, 1);
            cols.splice(new_index, 0, col);
        }
    }
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", boot);
    } else {
        boot();
    }
})();