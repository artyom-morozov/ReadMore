import { Component, OnInit, OnDestroy } from "@angular/core";
import { Subscription } from "rxjs";
import { BooksApiService } from "./books/books-api.service";
import { Book } from "./books/book.model";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.css"]
})
export class AppComponent implements OnInit, OnDestroy {
  title = "app";
  booksListSubs: Subscription;
  booksList;

  constructor(private booksApi: BooksApiService) {}

  ngOnInit() {
    console.log("Init");
    this.booksListSubs = this.booksApi.getBooks().subscribe(res => {
      console.log(JSON.stringify(res) + " title " + res[0].title);
      this.booksList = res;
    }, console.error);
  }

  ngOnDestroy() {
    this.booksListSubs.unsubscribe();
  }
}
