export class Book {
  constructor(
    public title: string,
    public author: string,
    public _id?: number,
    public updatedAt?: Date,
    public createdAt?: Date,
    public lastUpdatedBy?: string
  ) {}
}
