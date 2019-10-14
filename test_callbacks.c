#include <gtk/gtk.h>
#include <stdio.h>
#include "test_callbacks.h"

void on_button_clicked(GtkButton *btn, gpointer data) {
    // change button label when it's clicked
    //gtk_button_set_label(btn, "Hello World");
    // Print to stdout
    printf("Hello, World!\n");
}
