import * as util from "../util.tsx";
import * as objects from "../objects.tsx";

function CatalogFilter({
  filters,
  setFilters,
  updateFilters: updateFilters,
  properties,
  colors,
  priceMax,
  priceMin,
}: {
  filters: objects.CatalogFilters;
  setFilters: React.Dispatch<any>;
  updateFilters: (newFilters: objects.CatalogFilters) => void;
  properties: objects.Property[];
  colors: objects.Color[];
  priceMax: number;
  priceMin: number;
}) {
  return (
    <div style={{ display: "flex", flexDirection: "column" }}>
      <div style={{ display: "flex", flexDirection: "row", gap: "20px" }}>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
          }}
        >
          <label
            onClick={() =>
              setFilters({
                ...filters,
                productOnlyInStock: false,
              })
            }
          >
            Все товары
          </label>
          <input
            type="checkbox"
            checked={!filters.productOnlyInStock}
            onChange={(e) => {
              if (e.target.checked)
                setFilters({
                  ...filters,
                  productOnlyInStock: false,
                });
            }}
          />
        </div>
        <div style={{ display: "flex", flexDirection: "column" }}>
          <label
            onClick={() =>
              setFilters({
                ...filters,
                productOnlyInStock: true,
              })
            }
          >
            В наличии
          </label>
          <input
            type="checkbox"
            checked={filters.productOnlyInStock}
            onChange={(e) => {
              if (e.target.checked)
                setFilters({
                  ...filters,
                  productOnlyInStock: true,
                });
            }}
          />
        </div>
      </div>
      <div style={{ display: "flex", flexDirection: "row" }}>
        <input
          type="number"
          placeholder={String(priceMin)}
          value={
            filters.productPriceStart === 0 ? "" : filters.productPriceStart
          }
          onChange={(e) =>
            setFilters({
              ...filters,
              productPriceStart: util.Num(e.target.value),
            })
          }
        />
        <input
          type="number"
          placeholder={String(priceMax)}
          value={filters.productPriceEnd === 0 ? "" : filters.productPriceEnd}
          onChange={(e) =>
            setFilters({
              ...filters,
              productPriceEnd: util.Num(e.target.value),
            })
          }
        />
      </div>
      <div style={{ display: "flex", flexDirection: "column" }}>
        <h5>Colors:</h5>
        {colors.map((color) => (
          <div
            key={color.colorID}
            style={{ display: "flex", flexDirection: "row" }}
          >
            <label>{color.colorName}</label>
            <input
              type="checkbox"
              checked={filters.colors.includes(color.colorID)}
              onChange={(e) => {
                const newColors = structuredClone(filters.colors);
                e.target.checked
                  ? newColors.push(color.colorID)
                  : newColors.splice(newColors.indexOf(color.colorID), 1);

                setFilters({ ...filters, colors: newColors });
              }}
            />
          </div>
        ))}
      </div>
      {properties.map((property) => {
        let filterPropertyIndex = -1;
        for (let i = 0; i < filters.properties.length; i++) {
          if (filters.properties[i].propertyID == property.propertyID) {
            filterPropertyIndex = i;
            break;
          }
        }
        if (filterPropertyIndex == -1) {
          filterPropertyIndex = filters.properties.length;
          filters.properties.push({
            propertyID: property.propertyID,
            propertyValues: [],
          });
        }
        return (
          <div
            key={property.propertyID}
            style={{ display: "flex", flexDirection: "column" }}
          >
            <h5>{property.propertyName}:</h5>
            {property.propertyValues.map((value) => (
              <div
                key={
                  String(filters.properties[filterPropertyIndex].propertyID) +
                  value
                }
                style={{ display: "flex", flexDirection: "row" }}
              >
                <label>{value}</label>
                <input
                  type="checkbox"
                  checked={filters.properties[
                    filterPropertyIndex
                  ].propertyValues.includes(value)}
                  onChange={(e) => {
                    const newProperties = structuredClone(filters.properties);
                    e.target.checked
                      ? newProperties[filterPropertyIndex].propertyValues.push(
                          value,
                        )
                      : newProperties[
                          filterPropertyIndex
                        ].propertyValues.splice(
                          newProperties[
                            filterPropertyIndex
                          ].propertyValues.indexOf(value),
                          1,
                        );

                    setFilters({ ...filters, properties: newProperties });
                  }}
                />
              </div>
            ))}
          </div>
        );
      })}
      <button onClick={() => updateFilters(structuredClone(filters))}>
        Применить фильтры
      </button>
    </div>
  );
}

export default CatalogFilter;
