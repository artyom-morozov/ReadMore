import { BrowserModule } from "@angular/platform-browser";
import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from "@angular/core";
import { AppRoutingModule } from "./app-routing.module";
import { AppComponent } from "./app.component";
import { BooksApiService } from "./books/books-api.service";
import { HttpClient, HttpClientModule } from "@angular/common/http";

@NgModule({
  declarations: [AppComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  imports: [HttpClientModule, BrowserModule, AppRoutingModule],
  providers: [BooksApiService],
  bootstrap: [AppComponent]
})
export class AppModule {}
