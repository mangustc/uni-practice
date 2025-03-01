import * as objects from "../objects";
import * as requests from "../requests";
import { useEffect, useState, useRef } from "react";
import Card from "./card";

import { useDraggable } from "react-use-draggable-scroll";


export function ProductList({title, products} : {title: string, products:  objects.ProductCatalog[]}) {
  const [prev, setPrev] = useState(false);
  const [next, setNext] = useState(false);
  const scrollOffset = 219 + 40;

  useEffect(() => {
    if (products.length != 0) {
      setNext(true);
    }
  }, [products]);

  const ref = useRef<HTMLDivElement>(null) as React.MutableRefObject<HTMLDivElement>;
  const { events } = useDraggable(ref, {
    applyRubberBandEffect: true
  });

  const handleScroll = () => {
    if (ref.current) {
      if (ref.current.scrollLeft == 0) {
        setPrev(false);
      } else {
        setPrev(true);
      }
      if ((ref.current.clientWidth + ref.current.scrollLeft) == ref.current.scrollWidth) {
        setNext(false);
      } else {
        setNext(true);
      }
    }
  };

  function handleLeft() {
    if (ref.current) {
      const currentScrollPosition = ref.current.scrollLeft - scrollOffset;
      ref.current.scroll({
        left: currentScrollPosition,
        behavior: 'smooth'
      });
    }
  }

  function handleRight() {
    if (ref.current) {
      const currentScrollPosition = ref.current.scrollLeft + scrollOffset;
      ref.current.scroll({
        left: currentScrollPosition,
        behavior: 'smooth'
      });
    }
  }

  return (
    <div className="product-list-container">
      <div className="product-list-top">
        <h3>{title}</h3>
        <div style={{ display: "flex", gap: "16px" }}>
          {prev ? <div onClick={handleLeft} className="product-list-arrow-left"></div> : <div className="product-list-arrow-left-off"></div>}
          {next ? <div onClick={handleRight} className="product-list-arrow-right"></div> : <div className="product-list-arrow-right-off"></div>}
        </div>
      </div>
      <div className="product-list-scroll" ref={ref} {...events} onScroll={handleScroll}>
        {products.map((product, index) => (
          <Card
            key={index}
            productCatalog={product}
            photoSrc={`${requests.BACKEND_URL}/product/get_photo/${product.productID}`}
          />
        ))}
      </div>
    </div>
  );
};