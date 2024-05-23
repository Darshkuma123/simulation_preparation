<?xml version="1.0" encoding="UTF-8"?>
<xs:schema targetNamespace="http://example.com/ns/substation_template"
	xmlns:xs="http://www.w3.org/2001/XMLSchema" 
	xmlns="http://example.com/ns/substation_template">
    <xs:element name="substation_template">
        <!-- <xs:complexType>
            <xs:sequence>
              <xs:element name="object" type="infoType" maxOccurs="unbounded"/>
            </xs:sequence>
        </xs:complexType> -->
    </xs:element>
    <xs:element name="info" type="infoType"/>
    <xs:complexType name="infoType">
        <xs:sequence>
            <xs:element name="name" type="xs:string"/>
            <xs:element name="desc" type="xs:string"/>
        </xs:sequence>
    </xs:complexType>
    <xs:complexType name="Generator">
        <xs:sequence>
            <xs:element name="positionX" type="xs:string"/>
            <xs:element name="positionY" type="xs:string"/>
            <xs:element name="positionLength" type="xs:string"/>
            <xs:element name="positionWidth" type="xs:string"/>
            <xs:element name="Voltage" type="xs:string"/>
            <xs:element name="Power" type="xs:string"/>
        </xs:sequence>
        <xs:attribute name="id" type="xs:ID" use="required"/>
        <xs:attribute name="desc" type="xs:string" use="required"/>
    </xs:complexType>
     <xs:complexType name="Iso">
        <xs:sequence>
            <xs:element name="info" type="infoType"/>
            <xs:element name="positionX" type="xs:string"/>
            <xs:element name="positionY" type="xs:string"/>
            <xs:element name="positionLength" type="xs:string"/>
            <xs:element name="positionWidth" type="xs:string"/>
            <xs:element name="NormallyOpen" type="xs:string"/>
        </xs:sequence>
        <xs:attribute name="id" type="xs:ID" use="required"/>
        <xs:attribute name="desc" type="xs:string" use="required"/>
    </xs:complexType>
    <xs:complexType name="line">
        <xs:sequence>
            <xs:element name="info" type="infoType"/>
            <xs:element name="positionX" type="xs:string"/>
            <xs:element name="positionY" type="xs:string"/>
            <xs:element name="positionLength" type="xs:string"/>
            <xs:element name="positionWidth" type="xs:string"/>
            <xs:element name="value" type="xs:string"/>
        </xs:sequence>
        <xs:attribute name="id" type="xs:ID" use="required"/>
        <xs:attribute name="desc" type="xs:string" use="required"/>
    </xs:complexType>
     <xs:complexType name="feeder">
        <xs:sequence>
            <xs:element name="info" type="infoType"/>
            <xs:element name="positionX" type="xs:string"/>
            <xs:element name="positionY" type="xs:string"/>
            <xs:element name="positionLength" type="xs:string"/>
            <xs:element name="positionWidth" type="xs:string"/>
            <xs:element name="VoltageLevel" type="xs:string"/>
        </xs:sequence>
        <xs:attribute name="id" type="xs:ID" use="required"/>
        <xs:attribute name="desc" type="xs:string" use="required"/>
    </xs:complexType>
    <xs:complexType name="Load">
        <xs:sequence>
            <xs:element name="info" type="infoType"/>
            <xs:element name="positionX" type="xs:string"/>
            <xs:element name="positionY" type="xs:string"/>
            <xs:element name="positionLength" type="xs:string"/>
            <xs:element name="positionWidth" type="xs:string"/>
            <xs:element name="ActivePower" type="xs:string"/>
            <xs:element name="ReactivePower" type="xs:string"/>
        </xs:sequence>
        <xs:attribute name="id" type="xs:ID" use="required"/>
        <xs:attribute name="desc" type="xs:string" use="required"/>
    </xs:complexType>
        <xs:complexType name="TransFormer">
        <xs:sequence>
            <xs:element name="info" type="infoType"/>
            <xs:element name="positionX" type="xs:string"/>
            <xs:element name="positionY" type="xs:string"/>
            <xs:element name="positionLength" type="xs:string"/>
            <xs:element name="positionWidth" type="xs:string"/>
            <xs:element name="ActivePower" type="xs:string"/>
            <xs:element name="ReactivePower" type="xs:string"/>
        </xs:sequence>
        <xs:attribute name="id" type="xs:ID" use="required"/>
        <xs:attribute name="desc" type="xs:string" use="required"/>
    </xs:complexType>
    
</xs:schema>