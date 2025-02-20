import { useState } from "react";
import * as objects from "../objects";

export default function CatalogSort({
  currentSort,
  sorts,
  updateSort,
}: {
  currentSort: string;
  sorts: objects.CatalogSort[];
  updateSort: (newSort: string) => void;
}) {
  return (
    <div>
      <select value={currentSort} onChange={(e) => updateSort(e.target.value)}>
        {sorts.map((sort) => (
          <option key={sort.sortValue} value={sort.sortValue}>
            {sort.sortName}
          </option>
        ))}
      </select>
    </div>
  );
}
